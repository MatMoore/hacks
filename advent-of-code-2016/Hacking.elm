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
    , step : instruction -> state -> state
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


subscriptions : Model instruction state -> Sub Message
subscriptions { state, instructions } =
    if (List.length instructions) == 0 then
        Sub.none
    else
        every (100 * millisecond) (\t -> Step)


view { state, instructions } =
    p []
        [ text (instructions |> toString) ]


stepByStepProgram : ProgramFunctions instruction state -> Program Never (Model instruction state) Message
stepByStepProgram { init, instructions, step } =
    Html.program
        { init = ( { stepNo = 0, state = init, instructions = instructions }, Cmd.none )
        , view = view
        , update = update step
        , subscriptions = subscriptions
        }
