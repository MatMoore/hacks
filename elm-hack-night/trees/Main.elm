
import Html exposing (..)
import Tree
import TreeView


myTree =
    --Tree.empty
    Tree.map (\n -> n + 1) (Tree.fromList [3, 2, 1, 4])

main : Html
main =
    TreeView.draw 800 myTree
