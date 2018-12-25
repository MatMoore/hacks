module Day05 exposing (..)

import Html exposing (..)
import String exposing (..)
import List exposing (..)
import List.Extra exposing (group)
import Regex exposing (..)
import Debug exposing (..)
import Result
import Char exposing (..)
import MD5
import Time exposing (every)
import Array exposing (Array)


type Message
    = Step


input =
    "reyedfim"


testInput =
    "abc"


findFiveZeroHash : String -> Int -> List Char
findFiveZeroHash doorId integer =
    let
        plain =
            doorId ++ (toString integer)

        hash =
            MD5.hex plain
    in
        if startsWith "00000" hash then
            (log "Hash" hash) |> toList |> drop 5 |> take 2
        else
            []


buildPassword : State -> State
buildPassword state =
    case findFiveZeroHash state.doorId state.number of
        position :: char :: rest ->
            let
                idx =
                    log "idx" (String.toInt (String.fromChar position) |> Result.withDefault 8)

                value =
                    case Array.get idx state.foundDigits of
                        Just Nothing ->
                            Just char

                        Just a ->
                            a

                        Nothing ->
                            Nothing

                foundDigits =
                    Array.set idx value state.foundDigits

                digitsRemaining =
                    Array.filter (\val -> val == Nothing) foundDigits |> Array.length
            in
                { state | foundDigits = foundDigits, digitsRemaining = digitsRemaining, number = (state.number + 1) }

        _ ->
            { state | number = state.number + 1 }


type alias State =
    { foundDigits : Array (Maybe Char)
    , number : Int
    , doorId : String
    , digitsRemaining : Int
    }


init : State
init =
    { foundDigits = Array.repeat 8 Nothing
    , number = 1
    , doorId = input
    , digitsRemaining = 8
    }


update msg model =
    let
        buildMany =
            List.foldl (<<) identity (List.repeat 2000 buildPassword)
    in
        ( buildMany model, Cmd.none )


view model =
    div []
        [ "DECRYPTING: " ++ (model |> toString) |> text ]


subscriptions state =
    if state.digitsRemaining > 0 then
        every 0 (\t -> Step)
    else
        Sub.none


main =
    Html.program
        { init = ( init, Cmd.none )
        , view = view
        , update = update
        , subscriptions = subscriptions
        }
