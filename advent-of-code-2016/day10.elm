module Day10 exposing (..)

import Html exposing (..)
import Array exposing (..)
import Regex exposing (regex, find, HowMany(AtMost))
import Dict exposing (Dict)
import Time exposing (every, second, millisecond)
import String exposing (toInt)
import Result exposing (withDefault)


type Message
    = Step


type alias Microchip =
    Int


type alias Bin =
    List Microchip


type alias Bot =
    { lowest : Maybe Microchip, other : Maybe Microchip, errors : List String }


type Transfer
    = GiveToBot Int
    | PutInBin Int


type alias GiveInstruction =
    { high : Maybe Transfer
    , low : Maybe Transfer
    }


type Instruction
    = DoTransfer Int GiveInstruction
    | Input Int Int


type alias Bots =
    Dict Int Bot


type alias Bins =
    Dict Int Bin


type alias Model =
    { bots : Bots
    , bins : Bins
    , instructions : List Instruction
    }


testInput =
    """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


inputRegex =
    regex "value (\\d+) goes to bot (\\d+)"


giveRegex =
    regex "bot (\\d+) gives (?:low to (bot|output) (\\d+))?(?: and )?(?:high to (bot|output) (\\d+))?"


parseInputInstruction : String -> Result String Instruction
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


parseTarget : Maybe String -> Maybe String -> Maybe Transfer
parseTarget targetType targetNumber =
    case targetType of
        Just "bot" ->
            Maybe.andThen (Result.toMaybe << toInt) targetNumber
                |> Maybe.map GiveToBot

        Just "output" ->
            Maybe.andThen (Result.toMaybe << toInt) targetNumber
                |> Maybe.map PutInBin

        _ ->
            Nothing


parseGiveInstruction : String -> Result String Instruction
parseGiveInstruction string =
    case find (AtMost 1) giveRegex string of
        [ match ] ->
            case match.submatches of
                [ Just fromBot, lowTarget, lowNumber, highTarget, highNumber ] ->
                    let
                        highTransfer =
                            parseTarget highTarget highNumber

                        lowTransfer =
                            parseTarget lowTarget lowNumber
                    in
                        toInt fromBot
                            |> Result.map
                                (\botNumber -> DoTransfer botNumber { high = highTransfer, low = lowTransfer })

                _ ->
                    Err "Broken regex"

        _ ->
            Err "No match"


parseInstruction : String -> Result String Instruction
parseInstruction string =
    case parseInputInstruction string of
        Ok instruction ->
            Ok instruction

        _ ->
            parseGiveInstruction string


parsedInstructions =
    String.lines testInput |> List.filterMap (Result.toMaybe << parseInstruction)


giveToBot : Microchip -> Bot -> Result String Bot
giveToBot chip bot =
    case ( bot.lowest, bot.other ) of
        ( Just a, Nothing ) ->
            if chip >= a then
                Ok { bot | other = Just chip }
            else
                Ok { bot | lowest = Just chip, other = Just a }

        ( Nothing, Nothing ) ->
            Ok { bot | lowest = Just chip }

        ( Just a, Just b ) ->
            Err "Already holding two chips"

        ( Nothing, Just a ) ->
            giveToBot chip { bot | lowest = Just a, other = Nothing }


takeFromBot : Microchip -> Bot -> Result String Bot
takeFromBot chip bot =
    case ( bot.lowest, bot.other ) of
        ( Just a, Nothing ) ->
            if a == chip then
                Ok { bot | lowest = Nothing }
            else
                Err "Not holding chip"

        ( Just a, Just b ) ->
            if a == chip then
                Ok { bot | lowest = Just b, other = Nothing }
            else if b == chip then
                Ok { bot | lowest = Just a, other = Nothing }
            else
                Err "Not holding chip"

        ( Nothing, Nothing ) ->
            Err "Not holding anything"

        ( Nothing, Just a ) ->
            takeFromBot chip { bot | lowest = Just a, other = Nothing }


init : ( Model, Cmd Message )
init =
    ( { instructions = parsedInstructions
      , bins = Dict.empty
      , bots = Dict.empty
      }
    , Cmd.none
    )


stepThrough : (Model -> Model) -> Message -> Model -> ( Model, Cmd Message )
stepThrough stepFunction Step model =
    ( stepFunction model, Cmd.none )


newBot : Bot
newBot =
    { lowest = Nothing, other = Nothing, errors = [] }



{- TODO make lowest and other a result? -}


maybeGiveToBot : Int -> Maybe Bot -> Maybe Bot
maybeGiveToBot chip existing =
    let
        before =
            existing |> Maybe.withDefault newBot

        result =
            giveToBot chip before
    in
        case result of
            Ok after ->
                Just after

            Err msg ->
                Just { before | errors = msg :: before.errors }


maybeTakeFromBot : Int -> Maybe Bot -> Maybe Bot
maybeTakeFromBot chip existing =
    let
        before =
            existing |> Maybe.withDefault newBot
    in
        case (takeFromBot chip before) of
            Ok new ->
                Just new

            Err msg ->
                Just { before | errors = msg :: before.errors }


runInstruction : Model -> Model
runInstruction model =
    case model.instructions of
        head :: tail ->
            case head of
                DoTransfer bot gifts ->
                    model

                Input bot value ->
                    model

        _ ->
            model


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
