class Camera(object):
	def receive(r):
		loaded_r = json.loads(r)
		return loaded_r['time'], loaded_r['frame']

	def get_name(self):
		name, frame = self.receive(r)
		# save frame
		return name

	def get_frame(self):
		name = self.get_name()
		self.frames = open(name + '.jpg', 'rb').read()
		return self.frames
