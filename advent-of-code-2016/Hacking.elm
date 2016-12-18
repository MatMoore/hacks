module Hacking exposing (stepByStepProgram)

import Html exposing (..)
import Array exposing (..)
import Regex exposing (regex, find, HowMany(AtMost))
import Dict exposing (Dict)
import Time exposing (every, second, millisecond)
import String exposing (toInt)
import Result exposing (withDefault)


type Message
    = Step


type alias ProgramFunctions instruction state =
    { init : state
    , instructions : List instruction
    , step : Maybe (instruction -> state -> state)
    , view : Maybe (Model instruction state -> Html Message)
    , delayMs : Maybe Float
    }


type alias Model instruction state =
    { stepNo : Int
    , state : state
    , instructions : List instruction
    }


update : (instruction -> state -> state) -> Message -> Model instruction state -> ( Model instruction state, Cmd Message )
update stepFunction Step { stepNo, state, instructions } =
    case instructions of
        first :: rest ->
            ( { stepNo = (stepNo + 1), state = (stepFunction first state), instructions = rest }, Cmd.none )

        _ ->
            ( { stepNo = stepNo, state = state, instructions = instructions }, Cmd.none )


subscriptions : Float -> Model instruction state -> Sub Message
subscriptions delayMs { state, instructions } =
    if (List.length instructions) == 0 then
        Sub.none
    else
        every (delayMs * millisecond) (\t -> Step)


viewInstructions instructions =
    ul []
        (List.map
            (toString >> text >> (\text -> li [] [ text ]))
            instructions
        )


viewState state =
    p [] [ state |> toString |> text ]


defaultView { state, instructions } =
    div
        []
        [ viewState state
        , viewInstructions instructions
        ]


defaultStep instruction state =
    state


stepByStepProgram : ProgramFunctions instruction state -> Program Never (Model instruction state) Message
stepByStepProgram { init, instructions, step, view, delayMs } =
    Html.program
        { init = ( { stepNo = 0, state = init, instructions = instructions }, Cmd.none )
        , view = view |> Maybe.withDefault defaultView
        , update = update (step |> Maybe.withDefault defaultStep)
        , subscriptions = subscriptions (delayMs |> Maybe.withDefault 0)
        }
