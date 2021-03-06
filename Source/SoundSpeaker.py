###############################################################################
#             Mouse Click Controller | Template v 1.0 | UPBGE 0.2.3           #
###############################################################################
#                      Created by: Guilherme Teres Nunes                      #
#                       Access: youtube.com/UnidayStudio                      #
#                               github.com/UnidayStudio                       #
###############################################################################
# This component will serve as an sound Speaker for your game. With this, you
# can easly control 3D sound, volume.
# Unfortunatelly, the sounds needs to be mono to make the 3D sound works.
# You can convert to mono using windows CMD like this:
# > ffmpeg -i Sound.wav -ac 1 SoundMono.wav
###############################################################################
import bge
import aud

class SoundSpeaker(bge.types.KX_PythonComponent):
	args = {
		"Sound File"	: "",
		"Loop Sound"	: True,
		"Volume"		: 1.0,
		"Pitch"			: 1.0,
		"3D Sound"		: True,
		"Min Distance"	: 1.0,
		"Max Distance"	: 100.0,
		"Delete Object After End"	: False,
	}

	# Start Function
	def start(self, args):
		scene = bge.logic.getCurrentScene()
		cam = scene.active_camera

		# Loading the device...
		self.device  = aud.device()
		self.device.distance_model = aud.AUD_DISTANCE_MODEL_LINEAR

		# Loading the sound...
		sName = bge.logic.expandPath("//")+args["Sound File"]
		self.factory = aud.Factory(sName)

		# Playing the sound...
		self.handle = self.device.play(self.factory)

		# 3D Sound configuration...
		self.__3dSound = args["3D Sound"]
		self.handle.relative = (self.__3dSound == False)
		self.handle.distance_maximum   = abs(args["Max Distance"])
		self.handle.distance_reference = abs(args["Min Distance"])
		self.handle.pitch = args["Pitch"]

		self.handle.volume = args["Volume"]

		if args["Loop Sound"]:
			self.handle.loop_count = -1
		else:
			self.handle.loop_count = 0

		self.__deleteObj = args["Delete Object After End"]

	# Function to pause the sound
	def PauseSound(self):
		self.handle.pause()

	# Function to resume the sound
	def ResumeSound(self):
		self.handle.resume()

	# Function to stop the sound (and delete the object)
	def StopSound(self):
		self.handle.stop()
		if self.__deleteObj:
			self.object.endObject()

	# Update Function
	def update(self):
		scene = bge.logic.getCurrentScene()
		cam = scene.active_camera

		if self.__3dSound:
			self.device.listener_location   = cam.worldPosition
			self.device.listener_orientation= cam.worldOrientation.to_quaternion()
			try:
				self.handle.location = self.object.worldPosition
			except:
				if self.__deleteObj:
					self.object.endObject()

