#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key=None, value=None, is_virtual=False):
		self.key = key
		self.value = value
		self.is_virtual = is_virtual
		self.parent = None
		if is_virtual:
			self.left = None
			self.right = None
			self.height = -1
		else:
			self.left = AVLNode(is_virtual=True)
			self.right = AVLNode(is_virtual=True)
			self.height = 0
		

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return not self.is_virtual


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self):
		self.root = AVLNode(is_virtual=True)
		self.treeSize = 0


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		return None, -1


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		return None, -1


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		return None, -1, -1


	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree
`
	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	# Runtime: O(log n)
	def join(self, tree2, key, val):
		size_self = self.treeSize
		size_tree2 = tree2.treeSize

		# handle empty trees: result will reside in self
		if not self.root.is_real_node():
			# insert separating key into tree2 and make that the result
			tree2.insert(key, val)
			self.root = tree2.root
			self.treeSize = tree2.treeSize
			return

		if not tree2.root.is_real_node():
			# insert separating key into self
			self.insert(key, val)
			self.treeSize = self.treeSize
			return

		# determine which tree holds keys < key (left) and which > key (right)
		max_self = self.max_node()
		max_tree2 = tree2.max_node()


		if max_self.key < key:
			left, right = self, tree2
		elif max_tree2.key < key:
			left, right = tree2, self
		else:
			raise ValueError("Precondition violated: one tree must have all keys < key and the other > key")

		# heights of the two trees (use -1 for empty)
		h_left = left.root.height if left.root.is_real_node() else -1
		h_right = right.root.height if right.root.is_real_node() else -1

		# equal heights -> new root between them
		if h_left == h_right:
			new_root = AVLNode(key, val)
			# attach left and right subtrees appropriately
			new_root.left = left.root
			new_root.right = right.root
			if new_root.left.is_real_node():
				new_root.left.parent = new_root
			if new_root.right.is_real_node():
				new_root.right.parent = new_root
			new_root.height = h_left + 1
			self.root = new_root

			self.fixUpwards(new_root) # TODO make sure its implemented with that name!
			self.treeSize = size_self + size_tree2 + 1
			return

		# ensure taller holds the taller tree
		if h_left > h_right:
			taller, shorter, taller_is_left = left, right, True
		else:
			taller, shorter, taller_is_left = right, left, False

		# let the taller tree attach the shorter along the correct spine
		taller._join_with_shorter(shorter, key, val, taller_is_left)
		self.root = taller.root
		self.treeSize = size_self + size_tree2 + 1
		return
	
	def _join_with_shorter(self, shorter, key, val, self_is_left):
		"""Attach a separating node (key,val) between self (the taller tree) and shorter.
		self_is_left indicates whether self's keys are all < key (so we walk right spine),
		otherwise we walk left spine.
	After attachment, call self.fixUpwards(new_node) (assumed implemented elsewhere).
	"""
		# Runtime: O(log n)
		h_short = shorter.root.height if shorter.root.is_real_node() else -1
		current = self.root if self.root.is_real_node() else AVLNode(is_virtual=True)
		parent = None

		if self_is_left:
			# walk down the right spine until current.height <= h_short
			while current.is_real_node() and current.height > h_short:
				parent = current
				current = current.right
			# create and attach new node
			new_node = AVLNode(key, val)
			new_node.left = current
			if current.is_real_node():
				current.parent = new_node
			new_node.right = shorter.root
			if shorter.root.is_real_node():
				shorter.root.parent = new_node

			if parent is not None:
				parent.right = new_node
				new_node.parent = parent
			else:
				# attach as new root of this taller tree
				self.root = new_node
				new_node.parent = None
		else:
			# walk down the left spine
			while current.is_real_node() and current.height > h_short:
				parent = current
				current = current.left
			new_node = AVLNode(key, val)
			new_node.right = current
			if current.is_real_node():
				current.parent = new_node
			new_node.left = shorter.root
			if shorter.root.is_real_node():
				shorter.root.parent = new_node

			if parent is not None:
				parent.left = new_node
				new_node.parent = parent
			else:
				self.root = new_node
				new_node.parent = None

		# provisional height for the new node (proper heights/balancing done by fixUpwards)
		left_h = new_node.left.height if new_node.left.is_real_node() else -1
		right_h = new_node.right.height if new_node.right.is_real_node() else -1
		new_node.height = 1 + max(left_h, right_h)

		self.fixUpwards(new_node) #TODO make sure its implemented with that name!!!!
		return


	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	# Runtime: O(log n)
	def split(self, node):
		# defensive: if node is None return two empty trees
		if node is None or not node.is_real_node():
			return AVLTree(), AVLTree()

		left_tree, right_tree = self._recSplit(self.root, node.key)
		# make the original tree unusable per spec
		self.root = AVLNode(is_virtual=True)
		return left_tree, right_tree


	def _recSplit(self, v, key):
		"""
		Recursive helper. Returns (left_tree, right_tree) where:
		left_tree  contains all keys < key in subtree rooted at v
		right_tree contains all keys > key
		"""
		# Runtime: O(log n)
		# base case: empty subtree
		if not v.is_real_node():
			return AVLTree(), AVLTree()

		# exact split at v
		if v.key == key:
			left_tree = AVLTree()
			right_tree = AVLTree()

			left_tree.root = v.left
			if left_tree.root.is_real_node():
				left_tree.root.parent = None

			right_tree.root = v.right
			if right_tree.root.is_real_node():
				right_tree.root.parent = None

			# detach v itself
			v.left = AVLNode(is_virtual=True)
			v.right = AVLNode(is_virtual=True)
			v.parent = None
			return left_tree, right_tree

		# key is in the left subtree
		if key < v.key:
			# split the left child
			T1, Tmid = self._recSplit(v.left, key)

			# build T2 = Join(Tmid, v, v.right)
			right_sub = AVLTree()
			right_sub.root = v.right
			if right_sub.root.is_real_node():
				right_sub.root.parent = None

			# Tmid holds keys (key, v.key); right_sub holds keys > v.key
			# So Tmid < v.key < right_sub
			if not Tmid.root.is_real_node():
				# no Tmid: create a tree with v as root and right_sub as right child
				T2 = AVLTree()
				new_root = AVLNode(v.key, v.value)
				new_root.right = right_sub.root
				if new_root.right.is_real_node():
					new_root.right.parent = new_root
				new_root.parent = None
				# compute height safely (child height fallback = -1)
				left_h = new_root.left.height if new_root.left.is_real_node() else -1
				right_h = new_root.right.height if new_root.right.is_real_node() else -1
				new_root.height = 1 + max(left_h, right_h)
				T2.root = new_root
				# optionally: self.fixUpwards(new_root)
			else:
				Tmid.join(right_sub, v.key, v.value)
				T2 = Tmid

			# detach original v
			v.left = AVLNode(is_virtual=True)
			v.right = AVLNode(is_virtual=True)
			v.parent = None
			return T1, T2

		# key is in the right subtree (key > v.key)
		else:
			# split the right child
			Tmid, T2 = self._recSplit(v.right, key)

			# build T1 = Join(v.left, v, Tmid)
			left_sub = AVLTree()
			left_sub.root = v.left
			if left_sub.root.is_real_node():
				left_sub.root.parent = None

			if not Tmid.root.is_real_node():
				T1 = AVLTree()
				new_root = AVLNode(v.key, v.value)
				new_root.left = left_sub.root
				if new_root.left.is_real_node():
					new_root.left.parent = new_root
				new_root.right = AVLNode(is_virtual=True)
				new_root.parent = None
				# compute height safely
				left_h = new_root.left.height if new_root.left.is_real_node() else -1
				right_h = new_root.right.height if new_root.right.is_real_node() else -1
				new_root.height = 1 + max(left_h, right_h)
				T1.root = new_root
				# optionally: self.fixUpwards(new_root)
			else:
				left_sub.join(Tmid, v.key, v.value)
				T1 = left_sub

			v.left = AVLNode(is_virtual=True)
			v.right = AVLNode(is_virtual=True)
			v.parent = None
			return T1, T2
	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	# Runtime: O(n)
	def avl_to_array(self):
		retArray,stack = [], []
		node = self.root 
		
		if not node.is_real_node():
			return retArray
		
		while stack or node.is_real_node():
			while node.is_real_node():
				stack.append(node)
				node = node.left
			node = stack.pop()
			retArray.append((node.key, node.value))
			node = node.right
		return retArray
	

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	# Runtime: O(log n)
	def max_node(self):
		node = self.root
		if not node.is_real_node():
			return None
		while node.right.is_real_node():
			node = node.right
		return node if node.is_real_node() else None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	# Runtime: O(1)
	def size(self):
		return self.treeSize #TODO need to update size in insert and delete methods	


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	# Runtime: O(1)
	def get_root(self):
		return self.root if self.root.is_real_node() else None
