module Tree where


type Tree a
    = Empty
    | Node a (Tree a) (Tree a)


empty : Tree a
empty =
  Empty


singleton : a -> Tree a
singleton el = Node el Empty Empty


insert : comparable -> Tree comparable -> Tree comparable
insert el tree =
  case tree of
    Node parent left right ->
      if el < parent then
        Node parent (insert el left) right
      else if el > parent then
        Node parent left (insert el right)
      else
        tree

    Empty ->
      singleton el



fromList : List comparable -> Tree comparable
fromList things = case things of
    [] -> Empty
    head :: tail -> fromList tail |> insert head



depth : Tree a -> Int
depth tree =
  case tree of
    Node parent left right ->
      1 + (depth left) + (depth right)
    Empty ->
      0


map : (a -> b) -> Tree a -> Tree b
map func tree = case tree of
    Empty -> Empty
    Node a left right -> Node (func a) (map func left) (map func right)


fold: (a -> b -> b) -> b -> Tree a -> b
fold func initial tree = case tree of
    Empty -> initial
    Node value left right ->
        fold func (
            fold func (func value initial) left
        ) right


foldNum : Tree Int -> Int
foldNum = fold (+) 0


flatten : Tree a -> List a
flatten tree =
  case tree of
    Empty ->
      []
    Node a left right -> a :: List.append (flatten left) (flatten right)

{-----------------------------------------------------------------

Exercises:

(1) Sum all of the elements of a tree.

       sum : Tree number -> number

(2) Flatten a tree into a list.

       flatten : Tree a -> List a

(3) Check to see if an element is in a given tree.

       contains : a -> Tree a -> Bool

(4) Write a general fold function that acts on trees. The fold
    function does not need to guarantee a particular order of
    traversal.

       fold : (a -> b -> b) -> b -> Tree a -> b

(5) Use "fold" to do exercises 1-3 in one line each. The best
    readable versions I have come up have the following length
    in characters including spaces and function name:
      sum: 16
      flatten: 21
      contains: 45
    See if you can match or beat me! Don't forget about currying
    and partial application!

(6) Can "fold" be used to implement "map" or "depth"?

(7) Try experimenting with different ways to traverse a
    tree: pre-order, in-order, post-order, depth-first, etc.
    More info at: http://en.wikipedia.org/wiki/Tree_traversal

-----------------------------------------------------------------}
