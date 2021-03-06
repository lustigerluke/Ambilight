
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread


class PiVideoStream:
	def __init__(self, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FRAMERATE, rotation, hflip, vflip):
		self._CAMERA_WIDTH = CAMERA_WIDTH
		self._CAMERA_HEIGHT= CAMERA_HEIGHT
		self._CAMERA_FRAMERATE = CAMERA_FRAMERATE
		self._rotation = rotation
		self._hflip = hflip
		self._vflip = vflip
		framerate=CAMERA_FRAMERATE
		resolution=(CAMERA_WIDTH, CAMERA_HEIGHT)
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.rotation = rotation
		self.camera.framerate = framerate
		self.camera.hflip = hflip
		self.camera.vflip = vflip
		self.camera.brightness = 40
		self.camera.exposure_mode = 'night'
		self.camera.awb_mode = 'shade'
		self.meter_mode = 'backlit'
		
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
		
			#~ vs.sharpness = 0
	#~ vs.contrast = 0
	#~ vs.brightness = 50
	#~ vs.saturation = 0
	#~ vs.ISO = 0
	#~ vs.video_stabilization = False
	#~ vs.exposure_compensation = 100		#
	#~ vs.exposure_mode = 'night'			#
	#~ vs.meter_mode = 'backlit'
	#~ vs.awb_mode = 'shade'				#
	#~ vs.image_effect = 'none'
	#~ vs.color_effects = None
	#~ vs.rotation = 0
	#~ vs.hflip = False
	#~ vs.vflip = False
	#~ vs.crop = (0.0, 0.0, 1.0, 1.0)	
		
		format="bgr", use_video_port=True)
	
	        # initialize the frame and the variable used to indicate
	        # if the thread should be stopped
		self.frame = None
		self.stopped = False
	
	def start(self):
		# start the thread to read frames from the video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self
	
	def update(self):
		# keep looping infinitely until the thread is stopped
		for f in self.stream:
			# grab the frame from the stream and clear the stream in
			# preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)
				# if the thread indicator variable is set, stop the thread
	            # and resource camera resources
	        if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return
	
	def read(self):
		# return the frame most recently read
		return self.frame
	
	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True
	
