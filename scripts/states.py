# AUTHORED by Devon Daley

class State(object):
	
	def __init__(self):
		print 'Current state: ', str(self)
		
	def on_event(self, event):
		pass
		
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		return self.__class__.__name__
		

class WallfollowState(State):
	"""
	The state where we are on the right path and following the wall.
	"""
	
	def on_event(self, event):
		if event == "bump":
			return AvoidanceState()
		if event == "newdest":
			return InterState()
		elif event == "dock":
			return DockState()
		return self


class AvoidanceState(State):
	"""
	The state where we bumped into something and need to go around it
	"""
	
	def on_event(self, event):
		if event == "foundwall":
			return WallfollowState()
		return self
		
		
class DockState(State):
	"""
	The state where we reached the final destination and want to dock to wait for new requests
	"""
	
	def on_event(self, event):
		if event == "newdest":
			return InterState()
		return self


class InterState(State):
	"""
	The state where we reached an intermediate destination and are moving onto the next node
	"""
	
	def on_event(self, event):
		if event == "dirconfirm":
			return WallfollowState()
		return self
