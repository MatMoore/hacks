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


input =
    "reyedfim"


testInput =
    "abc"


findFiveZeroHash : String -> Int -> Maybe Char
findFiveZeroHash doorId integer =
    let
        plain =
            doorId ++ (toString integer)

        hash =
            MD5.hex plain
    in
        if startsWith "00000" hash then
            hash |> toList |> drop 5 |> head
        else
            Nothing


buildPassword : String -> List Char -> Int -> Int -> Int -> String
buildPassword doorId foundDigits digitsRemaining startNumber endNumber =
    if (digitsRemaining == 0) || (startNumber >= endNumber) then
        String.fromList foundDigits
    else
        case findFiveZeroHash doorId startNumber of
            Just char ->
                buildPassword doorId (foundDigits ++ [ log "found" char ]) (digitsRemaining - 1) (startNumber + 1) endNumber

            Nothing ->
                buildPassword doorId foundDigits digitsRemaining (startNumber + 1) endNumber


model =
    (buildPassword input [] 8 1 10000000)


update msg model =
    model


view model =
    div []
        [ model |> toString |> text ]


main =
    beginnerProgram { model = model, view = view, update = update }
