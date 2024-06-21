from sqlalchemy import Engine, update, select
from sqlalchemy.orm import Session, defer
from sqlalchemy.sql.operators import or_

from typing import Any

from src.domain.user import User
from src.interface.repository.user import UserRepoInterface
from src.repository.sqla_models.models import UserModel, FriendshipRequestModel, FriendshipModel
from src.usecase.dto import QueryParametersDTO
from src.usecase.user.dto import UserUpdateDTO, UserDTO

from pkg.sqlalchemy.utils import get_first, get_all, formalize_filters


class UserRepo(UserRepoInterface):
    def __init__(self, engine: Engine):
        self.engine = engine


    def store(self, user: User) -> User:
        with Session(self.engine) as s:
            new_user = UserModel(**(user.to_dict()))

            s.add(new_user)

            s.commit()

            s.refresh(new_user)

        return User(**new_user._asdict(User))


    def get_by_id(self, id: int) -> User:
        with Session(self.engine) as s:
            query = (
                select(UserModel)
                .where(UserModel.id == id)
            )

            found_user = get_first(session=s, query=query)

        if found_user is None:
            return None

        return User(**found_user._asdict(User))


    def get_by_username(self, username: str) -> User:
        with Session(self.engine) as s:
            query = (
                select(UserModel)
                .where(UserModel.username == username)
            )

            found_user = get_first(session=s, query=query)

        if found_user is None:
            return None

        return User(**found_user._asdict(User))


    def update(self, id: int, update_user_dto: UserUpdateDTO) -> User:
        with Session(self.engine) as s:
            query = (
                update(UserModel)
                .where(UserModel.id == id)
                .values(**update_user_dto)
            )

            s.execute(query)

            s.commit()

            updated_user = s.get(UserModel, id)

        return User(**updated_user._asdict(User))


    def get_all(self, query_parameters_dto: QueryParametersDTO) -> list[UserDTO]:
        with Session(self.engine) as s:
            query = (
                select(UserModel)
                .options(
                    defer(
                        UserModel.passwordHash
                    )
                )
            )

            filters = query_parameters_dto.filters

            if filters is not None:
                filters = formalize_filters(filters, UserModel)
                query = query.filter(*filters)

            found_users = get_all(session=s, query=query)

        found_users_dto = [UserDTO(**user._asdict(User)) for user in found_users]

        return found_users_dto


    def delete(self, id: int) -> User:
        with Session(self.engine) as s:
            found_user = s.get(UserModel, id)

            s.delete(found_user)

            s.commit()

        return User(**found_user._asdict(User))


    def _send_friend_request(self, requesting_user_id: int, receiving_user_id: int):
        with Session(self.engine) as s:
            new_request = FriendshipRequestModel(
                requesting_user_id=requesting_user_id,
                receiving_user_id=receiving_user_id
            )

            s.add(new_request)
            s.commit()


    def add_friend(self, requesting_user_id: int, receiving_user_id: int) -> User:
        with Session(self.engine) as s:
            query = (
                select(FriendshipRequestModel)
                .filter_by(
                    requesting_user_id=receiving_user_id,
                    receiving_user_id=requesting_user_id
                )
            )
            friendship_request = get_first(s, query)

            if not friendship_request:
                self._send_friend_request(
                    requesting_user_id=requesting_user_id,
                    receiving_user_id=receiving_user_id
                )
            else:
                friendships = (
                    FriendshipModel(
                        user_1=requesting_user_id,
                        user_2=receiving_user_id
                    ),
                    FriendshipModel(
                        user_1=receiving_user_id,
                        user_2=requesting_user_id
                    )
                )

                s.add_all(friendships)

                s.delete(friendship_request)
                s.commit()

            friend = s.get(UserModel, receiving_user_id)

            return User(**friend._asdict(User))



    def delete_friend(self, user_id: int, friend_id: int) -> User:
        with Session(self.engine) as s:
            query_user_1 = (
                select(FriendshipModel)
                .filter_by(
                    user_1=user_id,
                    user_2=friend_id
                )
            )

            query_user_2 = (
                select(FriendshipModel)
                .filter_by(
                    user_1=friend_id,
                    user_2=user_id
                )
            )

            friendships = (get_first(s, query_user_1), get_first(s, query_user_2))

            for friendship in friendships:
                s.delete(friendship)

            s.commit()

            deleted_friend = s.get(UserModel, friend_id)
            return User(**deleted_friend._asdict(User))


    def get_friends(self, user_id: int) -> list[UserDTO]:
        with Session(self.engine) as s:
            friends_ids = self.get_friends_ids(user_id=user_id)

            query_friends = (
                select(UserModel)
                .filter(
                    UserModel.id.in_(
                        friends_ids
                    )
                )
                .options(
                    defer(
                        UserModel.passwordHash
                    )
                )
            )

            friends = get_all(s, query_friends)

            friends_dto = [UserDTO(**friend._asdict(User)) for friend in friends]
            return friends_dto


    def get_received_friend_requests(self, user_id: int) -> list[UserDTO]:
        with Session(self.engine) as s:
            requesting_user_ids = self.get_received_requests_friends_ids(user_id=user_id)

            query_requesting_users = (
                select(UserModel)
                .filter(
                    UserModel.id.in_(
                        requesting_user_ids
                    )
                )
                .options(
                    defer(
                        UserModel.passwordHash
                    )
                )
            )

            requesting_users = get_all(s, query_requesting_users)

            found_users_dto = [UserDTO(**user._asdict(User)) for user in requesting_users]
            return found_users_dto


    def get_sent_friend_requests(self, user_id: int) -> list[UserDTO]:
        with Session(self.engine) as s:
            receiving_user_ids = self.get_sent_requests_friends_ids(user_id=user_id)

            query_receiving_users = (
                select(UserModel)
                .filter(
                    UserModel.id.in_(
                        receiving_user_ids
                    )
                )
                .options(
                    defer(
                        UserModel.passwordHash
                    )
                )
            )

            receiving_users = get_all(s, query_receiving_users)

            found_users_dto = [UserDTO(**user._asdict(User)) for user in receiving_users]
            return found_users_dto


    def delete_sent_friend_request(self, requesting_user_id: int, receiving_user_id: int) -> User:
        with Session(self.engine) as s:
            query = (
                select(FriendshipRequestModel)
                .filter_by(
                    requesting_user_id=requesting_user_id,
                    receiving_user_id=receiving_user_id
                )
            )

            sent_request = get_first(s, query)

            s.delete(sent_request)
            s.commit()

            canceled_friend = s.get(UserModel, receiving_user_id)
            return User(**canceled_friend._asdict(User))


    def delete_received_friend_request(self, user_id: int, requesting_user_id: int) -> User:
        with Session(self.engine) as s:
            query = (
                select(FriendshipRequestModel)
                .filter_by(
                    receiving_user_id=user_id,
                    requesting_user_id=requesting_user_id
                )
            )

            request = get_first(s, query)

            s.delete(request)
            s.commit()

            rejected_user = s.get(UserModel, requesting_user_id)
            return User(**rejected_user._asdict(User))


    def get_already_requested_users_ids(self, user_id: int) -> list[int]:
        with Session(self.engine) as s:
            received_friend_request_users = self.get_sent_requests_friends_ids(user_id=user_id)

            already_friends_users = self.get_friends_ids(user_id=user_id)

            query = (
                select(UserModel.id)
                .filter(
                    or_(
                        UserModel.id.in_(received_friend_request_users),
                        UserModel.id.in_(already_friends_users)
                    )
                )
            )

            ids = get_all(s, query)
            return ids


    def get_friends_ids(self, user_id: int) -> list[int]:
        with Session(self.engine) as s:
            query = (
                select(FriendshipModel.user_2)
                .filter_by(
                    user_1=user_id
                )
            )

            friends_ids = get_all(s, query)

        return friends_ids


    def get_sent_requests_friends_ids(self, user_id: int) -> list[int]:
        with Session(self.engine) as s:
            query = (
                select(FriendshipRequestModel.receiving_user_id)
                .filter_by(
                    requesting_user_id=user_id
                )
            )

            ids = get_all(s, query)

            return ids


    def get_received_requests_friends_ids(self, user_id: int) -> list[int]:
        with Session(self.engine) as s:
            query = (
                select(FriendshipRequestModel.requesting_user_id)
                .filter_by(
                    receiving_user_id=user_id
                )
            )

            ids = get_all(s, query)

            return ids


    def is_field_exists(self, field: dict[str: Any]) -> bool:
        with Session(self.engine) as s:
            query = (
                select(UserModel.id)
                .filter_by(**field)
            )

            found_user = get_first(session=s, query=query)

        return found_user is not None
