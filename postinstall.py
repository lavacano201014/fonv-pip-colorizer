import shutil

def postinstall():
	# Main UI
	shutil.copy("src/fnvpc.ui", "dist/fnvpc.ui")
	shutil.copy("src/fnvpc_es.ui", "dist/fnvpc_es.ui")

	# INI UI
	shutil.copy("src/writeini.ui", "dist/writeini.ui")
	shutil.copy("src/writeini_es.ui", "dist/writeini_es.ui")

	# Language UI
	shutil.copy("src/language.ui", "dist/language.ui")

	# Graphics
	shutil.copy("src/color_wheel.png", "dist/color_wheel.png")
	shutil.copy("src/convert.png", "dist/convert.png")
	shutil.copy("src/paint.png", "dist/paint.png")
