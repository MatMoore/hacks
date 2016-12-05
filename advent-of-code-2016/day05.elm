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
    plain = doorId ++ (toString integer)
    hash = MD5.hex plain
  in
    if startsWith "00000" hash then
      hash |> toList |> drop 5 |> head
    else
      Nothing

buildPassword : String -> List Char -> Int -> Int -> String
buildPassword doorId foundDigits startNumber endNumber =
  if (List.length foundDigits == 8) || (startNumber >= endNumber) then
    String.fromList foundDigits
  else
    case log "result" (findFiveZeroHash doorId (log "num" startNumber)) of
      Just char ->
        buildPassword doorId (foundDigits ++ [char]) (startNumber + 1) endNumber
      Nothing ->
        buildPassword doorId foundDigits (startNumber + 1) endNumber


model = testInput

update msg model =
    model


view model =
    div []
        [(buildPassword model [] 1 5017309) |> toString |> text]


main =
    beginnerProgram { model = model, view = view, update = update }
