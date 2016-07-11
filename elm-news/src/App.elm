module App exposing (..)
import State
import Html.App
import View

main: Program Never
main =
    Html.App.program {
        init = State.init
        ,update = State.update
                     , subscriptions = State.subscriptions
                     , view = View.root
                 }
