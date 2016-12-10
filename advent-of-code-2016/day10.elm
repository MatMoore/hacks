module Day10 exposing (..)

import Html exposing (..)
import Array exposing (..)
import Regex exposing (regex, find, HowMany(AtMost))
import Dict exposing (Dict)
import Time exposing (every, second, millisecond)
import String exposing (toInt)
import Result exposing (withDefault)


type alias Microchip =
    Int


type alias Bin =
    List Microchip


type alias Bot =
    { lowest : Maybe Microchip, other : Maybe Microchip }


testInput =
    """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


type Task
    = GiveToBot Int
    | PutInBin Int


type alias GiveInstruction =
    { high : Maybe Task
    , low : Maybe Task
    }


type Instruction
    = Transfer Int GiveInstruction
    | Input Int Int


inputRegex =
    regex "value (\\d+) goes to bot (\\d+)"


giveRegex =
    regex "bot (\\d+) gives (?:low to (bot|output) (\\d+))?(?: and )?(?:high to (bot|output) (\\d+))?"


parseInputInstruction string =
    case find (AtMost 1) inputRegex string of
        [ match ] ->
            case match.submatches of
                [ Just value, Just bot ] ->
                    case ( toInt value, toInt bot ) of
                        ( Ok intValue, Ok intBot ) ->
                            Ok (Input intBot intValue)

                        _ ->
                            Err "Can't convert values to int"

                _ ->
                    Err "Broken regex"

        _ ->
            Err "Not found"


parseGiveInstruction string =
    case find (AtMost 1) giveRegex string of
        [ match ] ->
            case match.submatches of
                [ Just fromBot, lowTarget, lowNumber, highTarget, highNumber ] ->
                    let
                        highTask =
                            case highTarget of
                                Just "bot" ->
                                    Maybe.andThen (Result.toMaybe << toInt) highNumber
                                        |> Maybe.map GiveToBot

                                Just "output" ->
                                    Maybe.andThen (Result.toMaybe << toInt) highNumber
                                        |> Maybe.map PutInBin

                                _ ->
                                    Nothing

                        lowTask =
                            case lowTarget of
                                Just "bot" ->
                                    Maybe.andThen (Result.toMaybe << toInt) lowNumber
                                        |> Maybe.map GiveToBot

                                Just "output" ->
                                    Maybe.andThen (Result.toMaybe << toInt) lowNumber
                                        |> Maybe.map PutInBin

                                _ ->
                                    Nothing
                    in
                        toInt fromBot
                            |> Result.map
                                (\botNumber -> Transfer botNumber { high = highTask, low = lowTask })

                _ ->
                    Err "Broken regex"

        _ ->
            Err "No match"


parseInstruction string =
    case parseInputInstruction string of
        Ok instruction ->
            Ok instruction

        _ ->
            parseGiveInstruction string


parsedInstructions =
    String.lines testInput |> List.filterMap (Result.toMaybe << parseInstruction)


giveBot : Microchip -> Bot -> Result String Bot
giveBot chip bot =
    case ( bot.lowest, bot.other ) of
        ( Just a, Nothing ) ->
            if chip >= a then
                Ok { bot | other = Just chip }
            else
                Ok { lowest = Just chip, other = Just a }

        ( Nothing, Nothing ) ->
            Ok { bot | lowest = Just chip }

        ( Just a, Just b ) ->
            Err "Already holding two chips"

        ( Nothing, Just a ) ->
            giveBot chip { bot | lowest = Just a, other = Nothing }


type alias Bots =
    Dict Int Bot


type alias Bins =
    Dict Int Bin


type alias Model =
    { bots : Bots
    , bins : Bins
    , instructions : List Instruction
    }


init : ( Model, Cmd Message )
init =
    ( { instructions = parsedInstructions
      , bins = Dict.empty
      , bots = Dict.empty
      }
    , Cmd.none
    )


type Message
    = Step


stepThrough : (Model -> Model) -> Message -> Model -> ( Model, Cmd Message )
stepThrough stepFunction Step model =
    ( stepFunction model, Cmd.none )


update : Message -> Model -> ( Model, Cmd Message )
update =
    stepThrough identity


subscriptions model =
    if (List.length model.instructions) == 0 then
        Sub.none
    else
        every (100 * millisecond) (\t -> Step)


view model =
    p []
        [ text (model.instructions |> toString) ]


main =
    program { init = init, view = view, update = update, subscriptions = subscriptions }
