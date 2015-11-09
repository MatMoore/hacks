
import Html exposing (..)
import Tree
import TreeView


myTree =
  Tree.empty
    |> Tree.insert 42
    |> Tree.insert 41
    |> Tree.insert 2
    |> Tree.insert 3
    |> Tree.insert 434


main : Html
main =
    TreeView.draw 800 myTree
