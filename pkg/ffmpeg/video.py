from subprocess import call


QUALITIES = {
	'360p': 'nhd',
	'480p': 'hd480',
	'720p': 'hd720',
	'1080p': 'hd1080'
}


# returns 0 (ok) or 1 (error)
def transcode(input: str, output: str, quality: str) -> int:
	command = f'ffmpeg -y -i { input } -preset veryslow -c:v libx264 -s { QUALITIES[quality] } -crf 20 -pix_fmt yuv420p -c:a copy -movflags +faststart { output }'
	exit_code = call(command, shell=True)
	
	return exit_code