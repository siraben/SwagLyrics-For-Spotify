import argparse
import time
import os
import random
import webbrowser
import threading
from swaglyrics.cli import lyrics, clear
from swaglyrics import spotify
from swaglyrics.tab import app


def main():
	parser = argparse.ArgumentParser(
		description="Get lyrics for the currently playing song on Spotify. Either --tab or --cli is required.")

	parser.add_argument('-t', '--tab', action='store_true', help='Display lyrics in a browser tab.')
	parser.add_argument('-c', '--cli', action='store_true', help='Display lyrics in the command-line.')

	args = parser.parse_args()

	if args.tab:
		print('Firing up a browser tab!')
		app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
		app.static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
		port = 5000 + random.randint(0, 999)
		url = "http://127.0.0.1:{0}".format(port)
		threading.Timer(1.25, lambda: webbrowser.open(url)).start()
		app.run(port=port)

	elif args.cli:
		song = spotify.song()  # get currently playing song
		artist = spotify.artist()  # get currently playing artist
		print(lyrics(song, artist))
		print('\n(Press Ctrl+C to quit)')
		while True:
			# refresh every 5s to check whether song changed
			# if changed, display the new lyrics
			try:
				if song == spotify.song() and artist == spotify.artist():
					time.sleep(5)
				else:
					song = spotify.song()
					artist = spotify.artist()
					if song and artist is not None:
						clear()
						print(lyrics(song, artist))
						print('\n(Press Ctrl+C to quit)')
			except KeyboardInterrupt:
				exit()

	else:
		parser.print_help()


if __name__ == '__main__':
	main()
