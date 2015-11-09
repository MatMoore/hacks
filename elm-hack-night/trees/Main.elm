
import Html exposing (..)
import Tree
import TreeView


myTree =
    --Tree.empty
    Tree.fromList [3, 2, 1, 4]

main : Html
main =
    TreeView.draw 800 myTree
