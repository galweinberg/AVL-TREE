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
	def __init__(self, key, value, is_virtual=False):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		# Virtual nodes represent the "null" children required by the assignment.
		# They have height -1, while real leaves start at height 0.
		self.is_virtual = is_virtual
		self.height = -1 if is_virtual else 0
	
	# Treat virtual nodes as falsy so existing code that checks "if node:"
	# behaves naturally with explicit virtual children.
	def __bool__(self):
		return self.is_real_node()
		

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
		self.root = None
		self.treeSize = 0


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		if self.root is None:
			return None, 1

		node = self.root
		edges = 0

		while node and node.is_real_node() and node.key != key:
			if key < node.key:
				node = node.left
			else:
				node = node.right
			edges += 1

		return (node if node and node.is_real_node() else None, edges + 1)


	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		if self.root is None:
			return None, 1

		start = self.max_node()
		node = start
		edges = 0

		# climb up from max until we find an ancestor whose parent is not strictly larger
		while node.parent and key < node.parent.key:
			node = node.parent
			edges += 1

		# standard BST search from the chosen starting point
		current = node
		while current and current.is_real_node() and current.key != key:
			if key < current.key:
				current = current.left
			else:
				current = current.right
			edges += 1

		return (current if current and current.is_real_node() else None, edges + 1)


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
		# empty tree -> create root
		if self.root is None:
			new_node = AVLNode(key, val)
			new_node.left = self._virtual_node()
			new_node.right = self._virtual_node()
			new_node.left.parent = new_node
			new_node.right.parent = new_node
			self.root = new_node
			self.treeSize = 1
			return new_node, 1, 0

		current = self.root
		parent = None
		edges = 0

		while current and current.is_real_node():
			parent = current
			if key < current.key:
				current = current.left
			else:
				current = current.right
			edges += 1

		new_node = AVLNode(key, val)
		new_node.left = self._virtual_node()
		new_node.right = self._virtual_node()
		new_node.left.parent = new_node
		new_node.right.parent = new_node
		new_node.parent = parent

		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		promotes = self.fixUpwards(parent, count_promote=True)
		self.treeSize += 1

		return new_node, (edges if edges > 0 else 1), promotes


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
		if self.root is None:
			new_node = AVLNode(key, val)
			new_node.left = self._virtual_node()
			new_node.right = self._virtual_node()
			new_node.left.parent = new_node
			new_node.right.parent = new_node
			self.root = new_node
			self.treeSize = 1
			return new_node, 1, 0

		start = self.max_node()
		node = start
		edges = 0

		# climb up while key is smaller than the ancestor
		while node.parent and key < node.parent.key:
			node = node.parent
			edges += 1

		parent = None
		current = node
		while current and current.is_real_node():
			parent = current
			if key < current.key:
				current = current.left
			else:
				current = current.right
			edges += 1

		new_node = AVLNode(key, val)
		new_node.left = self._virtual_node()
		new_node.right = self._virtual_node()
		new_node.left.parent = new_node
		new_node.right.parent = new_node
		new_node.parent = parent

		if key < parent.key:
			parent.left = new_node
		else:
			parent.right = new_node

		promotes = self.fixUpwards(parent, count_promote=True)
		self.treeSize += 1

		return new_node, (edges if edges > 0 else 1), promotes


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		if node is None or not node.is_real_node():
			return

		# if node has two real children, swap with successor and delete the successor instead
		if node.left and node.right:
			successor = self._min_node(node.right)
			node.key, node.value = successor.key, successor.value
			node = successor

		child = node.left if node.left else node.right  # at most one real child

		if child and not child.is_real_node():
			child = None

		parent = node.parent

		if parent is None:
			# deleting the root
			if child:
				child.parent = None
				self.root = child
			else:
				self.root = None
			start_rebalance = child if child else None
		else:
			if parent.left is node:
				if child:
					parent.left = child
					child.parent = parent
				else:
					parent.left = self._virtual_node()
					parent.left.parent = parent
			else:
				if child:
					parent.right = child
					child.parent = parent
				else:
					parent.right = self._virtual_node()
					parent.right.parent = parent
			start_rebalance = parent

		self.treeSize = max(0, self.treeSize - 1)

		if start_rebalance:
			self.fixUpwards(start_rebalance, count_promote=False)
		return	
	
	# ----------------- Internal helpers -----------------
	def _virtual_node(self):
		return AVLNode(None, None, is_virtual=True)

	def _height(self, node):
		return node.height if node else -1

	def _update_height(self, node):
		node.height = 1 + max(self._height(node.left), self._height(node.right))

	def _balance_factor(self, node):
		return self._height(node.left) - self._height(node.right)

	def _rotate_left(self, x):
		y = x.right
		x.right = y.left
		if x.right is not None:
			x.right.parent = x
		y.parent = x.parent
		if y.parent is None:
			self.root = y
		elif y.parent.left is x:
			y.parent.left = y
		else:
			y.parent.right = y
		y.left = x
		x.parent = y
		self._update_height(x)
		self._update_height(y)
		return y

	def _rotate_right(self, y):
		x = y.left
		y.left = x.right
		if y.left is not None:
			y.left.parent = y
		x.parent = y.parent
		if x.parent is None:
			self.root = x
		elif x.parent.left is y:
			x.parent.left = x
		else:
			x.parent.right = x
		x.right = y
		y.parent = x
		self._update_height(y)
		self._update_height(x)
		return x

	def fixUpwards(self, node, count_promote=False):
		"""
		Restore AVL balance from node up to the root.

		@type node: AVLNode
		@param count_promote: whether to count Case-1 promotions (height increase without rotation)
		@rtype: int
		@returns: number of promotions encountered (0 if count_promote is False)
		"""
		promotions = 0
		current = node

		while current:
			prev_height = current.height
			self._update_height(current)
			balance = self._balance_factor(current)

			if balance > 1:
				if self._balance_factor(current.left) < 0:
					self._rotate_left(current.left)
				current = self._rotate_right(current)
			elif balance < -1:
				if self._balance_factor(current.right) > 0:
					self._rotate_right(current.right)
				current = self._rotate_left(current)
			else:
				if count_promote and current.height > prev_height:
					promotions += 1

			current = current.parent

		return promotions

	def _min_node(self, node):
		current = node
		while current.left and current.left.is_real_node():
			current = current.left
		return current
	
	def _subtree_size(self, node):
		"""Count real nodes in the given subtree (virtual and None nodes contribute 0)."""
		if node is None or not node.is_real_node():
			return 0
		return 1 + self._subtree_size(node.left) + self._subtree_size(node.right)

	
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
	def join(self, tree2, key, val):
		# handle empty trees: result will reside in self
		if self.root is None:
			# insert separating key into tree2 and make that the result
			tree2.insert(key, val)
			self.root = tree2.root
			# invalidate tree2 per spec
			tree2.root = None
			tree2.treeSize = 0
			# recompute size defensively
			self.treeSize = self._subtree_size(self.root)
			return

		if tree2.root is None:
			# insert separating key into self
			self.insert(key, val)
			self.treeSize = self._subtree_size(self.root)
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
		h_left = left.root.height if left.root else -1
		h_right = right.root.height if right.root else -1

		# equal heights -> new root between them
		if h_left == h_right:
			new_root = AVLNode(key, val)
			# attach left and right subtrees appropriately
			new_root.left = left.root
			new_root.right = right.root
			if new_root.left:
				new_root.left.parent = new_root
			if new_root.right:
				new_root.right.parent = new_root
			new_root.height = h_left + 1
			self.root = new_root

			self.fixUpwards(new_root) # TODO make sure its implemented with that name!
			tree2.root = None
			tree2.treeSize = 0
			self.treeSize = self._subtree_size(self.root)
			return

		# ensure taller holds the taller tree
		if h_left > h_right:
			taller, shorter, taller_is_left = left, right, True
		else:
			taller, shorter, taller_is_left = right, left, False

		# let the taller tree attach the shorter along the correct spine
		taller._join_with_shorter(shorter, key, val, taller_is_left)
		self.root = taller.root
		# make tree2 unusable after join
		tree2.root = None
		tree2.treeSize = 0
		# recompute size defensively to avoid stale counts
		self.treeSize = self._subtree_size(self.root)
		return
	
	def _join_with_shorter(self, shorter, key, val, self_is_left):
		"""Attach a separating node (key,val) between self (the taller tree) and shorter.
		self_is_left indicates whether self's keys are all < key (so we walk right spine),
		otherwise we walk left spine.
		After attachment, call self.fixUpwards(new_node) (assumed implemented elsewhere).
		"""
		h_short = shorter.root.height if shorter.root else -1
		current = self.root
		parent = None

		if self_is_left:
			# walk down the right spine until current.height <= h_short
			while current and current.height > h_short:
				parent = current
				current = current.right
			# create and attach new node
			new_node = AVLNode(key, val)
			new_node.left = current
			if current:
				current.parent = new_node
			new_node.right = shorter.root
			if shorter.root:
				shorter.root.parent = new_node

			if parent:
				parent.right = new_node
				new_node.parent = parent
			else:
				# attach as new root of this taller tree
				self.root = new_node
				new_node.parent = None
		else:
			# walk down the left spine
			while current and current.height > h_short:
				parent = current
				current = current.left
			new_node = AVLNode(key, val)
			new_node.right = current
			if current:
				current.parent = new_node
			new_node.left = shorter.root
			if shorter.root:
				shorter.root.parent = new_node

			if parent:
				parent.left = new_node
				new_node.parent = parent
			else:
				self.root = new_node
				new_node.parent = None

		# ensure missing children are explicit virtual nodes for consistency
		if new_node.left is None:
			new_node.left = self._virtual_node()
			new_node.left.parent = new_node
		if new_node.right is None:
			new_node.right = self._virtual_node()
			new_node.right.parent = new_node

		self._update_height(new_node)

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
	def split(self, node):
		# defensive: if node is None return two empty trees
		if node is None:
			return AVLTree(), AVLTree()

		left_tree, right_tree = self._recSplit(self.root, node.key)
		# make the original tree unusable per spec
		self.root = None
		self.treeSize = 0
		# recompute sizes for the resulting trees to keep size() consistent
		left_tree.treeSize = self._subtree_size(left_tree.root)
		right_tree.treeSize = self._subtree_size(right_tree.root)
		return left_tree, right_tree


	def _recSplit(self, v, key):
		"""
		Recursive helper. Returns (left_tree, right_tree) where:
		left_tree  contains all keys < key in subtree rooted at v
		right_tree contains all keys > key
		"""
		# base case: empty subtree
		if v is None:
			return AVLTree(), AVLTree()

		# exact split at v
		if v.key == key:
			left_tree = AVLTree()
			right_tree = AVLTree()

			left_tree.root = v.left
			if left_tree.root:
				left_tree.root.parent = None

			right_tree.root = v.right
			if right_tree.root:
				right_tree.root.parent = None

			# detach v itself
			v.left = v.right = v.parent = None
			return left_tree, right_tree

		# key is in the left subtree
		if key < v.key:
			# split the left child
			T1, Tmid = self._recSplit(v.left, key)

			# build T2 = Join(Tmid, v, v.right)
			right_sub = AVLTree()
			right_sub.root = v.right
			if right_sub.root:
				right_sub.root.parent = None

			# Tmid holds keys (key, v.key); right_sub holds keys > v.key
			# So Tmid < v.key < right_sub
			if Tmid.root is None:
				# no Tmid: create a tree with v as root and right_sub as right child
				T2 = AVLTree()
				new_root = AVLNode(v.key, v.value)
				new_root.left = self._virtual_node()
				new_root.left.parent = new_root
				new_root.right = right_sub.root
				if new_root.right:
					new_root.right.parent = new_root
				new_root.parent = None
				# ensure right child exists as virtual if needed
				if new_root.right is None:
					new_root.right = self._virtual_node()
					new_root.right.parent = new_root
				self._update_height(new_root)
				T2.root = new_root
				# optionally: self.fixUpwards(new_root)
			else:
				Tmid.join(right_sub, v.key, v.value)
				T2 = Tmid

			# detach original v
			v.left = v.right = v.parent = None
			return T1, T2

		# key is in the right subtree (key > v.key)
		else:
			# split the right child
			Tmid, T2 = self._recSplit(v.right, key)

			# build T1 = Join(v.left, v, Tmid)
			left_sub = AVLTree()
			left_sub.root = v.left
			if left_sub.root:
				left_sub.root.parent = None

			if Tmid.root is None:
				T1 = AVLTree()
				new_root = AVLNode(v.key, v.value)
				new_root.left = left_sub.root
				if new_root.left:
					new_root.left.parent = new_root
				else:
					new_root.left = self._virtual_node()
					new_root.left.parent = new_root
				new_root.right = self._virtual_node()
				new_root.right.parent = new_root
				new_root.parent = None
				self._update_height(new_root)
				T1.root = new_root
				# optionally: self.fixUpwards(new_root)
			else:
				left_sub.join(Tmid, v.key, v.value)
				T1 = left_sub

			v.left = v.right = v.parent = None
			return T1, T2
	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		retArray,stack = [], []
		node = self.root 
		
		while stack or node:
			while node:
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
	def max_node(self):
		node = self.root
		if node is None:
			return None
		while node.right:
			node = node.right
		return node if node else None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary
	"""
	def size(self):
		return self.treeSize


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root if self.root else None
