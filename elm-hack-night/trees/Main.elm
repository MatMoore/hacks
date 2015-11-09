
import Html exposing (..)
import Tree
import TreeView


myTree =
    --Tree.empty
    Tree.fromList [1, 2, 3, 4]


main : Html
main =
    TreeView.draw 800 myTree
