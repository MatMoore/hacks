module Day08 exposing (..)

import Html exposing (..)
import Array exposing (Array)
import Time exposing (every, second)
import Regex exposing (..)
import String exposing (lines)
import Debug exposing (log)
import Dict exposing (Dict)

type Pixel = On | Off

type alias NumPixels = Int

type Instruction =
  RectOn NumPixels NumPixels
  | RotateRowRight Int NumPixels
  | RotateColumnDown Int NumPixels

type alias Grid = {width: Int, height: Int, pixels: Dict (Int, Int) Pixel}
type alias Model = {instructions: List Instruction, grid: Grid}

type Message = Step


input =
    """rect 1x1
rotate row y=0 by 6
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 5
rect 1x1
rotate row y=0 by 4
rect 2x1
rotate row y=0 by 5
rect 2x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 5
rect 4x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 3
rect 1x1
rotate row y=0 by 2
rect 1x1
rotate row y=0 by 6
rect 4x1
rotate row y=0 by 4
rotate column x=0 by 1
rect 3x1
rotate row y=0 by 6
rotate column x=0 by 1
rect 4x1
rotate column x=10 by 1
rotate row y=2 by 16
rotate row y=0 by 8
rotate column x=5 by 1
rotate column x=0 by 1
rect 7x1
rotate column x=37 by 1
rotate column x=21 by 2
rotate column x=15 by 1
rotate column x=11 by 2
rotate row y=2 by 39
rotate row y=0 by 36
rotate column x=33 by 2
rotate column x=32 by 1
rotate column x=28 by 2
rotate column x=27 by 1
rotate column x=25 by 1
rotate column x=22 by 1
rotate column x=21 by 2
rotate column x=20 by 3
rotate column x=18 by 1
rotate column x=15 by 2
rotate column x=12 by 1
rotate column x=10 by 1
rotate column x=6 by 2
rotate column x=5 by 1
rotate column x=2 by 1
rotate column x=0 by 1
rect 35x1
rotate column x=45 by 1
rotate row y=1 by 28
rotate column x=38 by 2
rotate column x=33 by 1
rotate column x=28 by 1
rotate column x=23 by 1
rotate column x=18 by 1
rotate column x=13 by 2
rotate column x=8 by 1
rotate column x=3 by 1
rotate row y=3 by 2
rotate row y=2 by 2
rotate row y=1 by 5
rotate row y=0 by 1
rect 1x5
rotate column x=43 by 1
rotate column x=31 by 1
rotate row y=4 by 35
rotate row y=3 by 20
rotate row y=1 by 27
rotate row y=0 by 20
rotate column x=17 by 1
rotate column x=15 by 1
rotate column x=12 by 1
rotate column x=11 by 2
rotate column x=10 by 1
rotate column x=8 by 1
rotate column x=7 by 1
rotate column x=5 by 1
rotate column x=3 by 2
rotate column x=2 by 1
rotate column x=0 by 1
rect 19x1
rotate column x=20 by 3
rotate column x=14 by 1
rotate column x=9 by 1
rotate row y=4 by 15
rotate row y=3 by 13
rotate row y=2 by 15
rotate row y=1 by 18
rotate row y=0 by 15
rotate column x=13 by 1
rotate column x=12 by 1
rotate column x=11 by 3
rotate column x=10 by 1
rotate column x=8 by 1
rotate column x=7 by 1
rotate column x=6 by 1
rotate column x=5 by 1
rotate column x=3 by 2
rotate column x=2 by 1
rotate column x=1 by 1
rotate column x=0 by 1
rect 14x1
rotate row y=3 by 47
rotate column x=19 by 3
rotate column x=9 by 3
rotate column x=4 by 3
rotate row y=5 by 5
rotate row y=4 by 5
rotate row y=3 by 8
rotate row y=1 by 5
rotate column x=3 by 2
rotate column x=2 by 3
rotate column x=1 by 2
rotate column x=0 by 2
rect 4x2
rotate column x=35 by 5
rotate column x=20 by 3
rotate column x=10 by 5
rotate column x=3 by 2
rotate row y=5 by 20
rotate row y=3 by 30
rotate row y=2 by 45
rotate row y=1 by 30
rotate column x=48 by 5
rotate column x=47 by 5
rotate column x=46 by 3
rotate column x=45 by 4
rotate column x=43 by 5
rotate column x=42 by 5
rotate column x=41 by 5
rotate column x=38 by 1
rotate column x=37 by 5
rotate column x=36 by 5
rotate column x=35 by 1
rotate column x=33 by 1
rotate column x=32 by 5
rotate column x=31 by 5
rotate column x=28 by 5
rotate column x=27 by 5
rotate column x=26 by 5
rotate column x=17 by 5
rotate column x=16 by 5
rotate column x=15 by 4
rotate column x=13 by 1
rotate column x=12 by 5
rotate column x=11 by 5
rotate column x=10 by 1
rotate column x=8 by 1
rotate column x=2 by 5
rotate column x=1 by 5"""


testInput =
    """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""

makeGrid: Int -> Int -> Grid
makeGrid gridWidth gridHeight =
  {width = gridWidth, height=gridHeight, pixels = Dict.empty}

init : (Model, Cmd Message)
init = ({instructions = lines testInput |> parseInstructions, grid = makeGrid 7 3}, Cmd.none)

parseInstructions: List String -> List Instruction
parseInstructions lines =
  List.filterMap parseInstruction lines

parseInstruction: String -> Maybe Instruction
parseInstruction string =
  let
    stringPairToInts (a, b) =
      case (String.toInt a |> Result.toMaybe, String.toInt b |> Result.toMaybe) of
        (Just a, Just b) -> Just (a, b)
        _ -> Nothing

    parseSubmatches submatches =
      case (log "" submatches) of
        [(Just "rect"), Just rectWidth, Just rectHeight, _, _] ->
          Just (rectWidth, rectHeight)
          |> Maybe.andThen stringPairToInts
          |> Maybe.map (\(x, y) -> RectOn x y)

        [(Just "rotate row"), _, _, Just row, Just amount] ->
          Just (row, amount)
          |> Maybe.andThen stringPairToInts
          |> Maybe.map (\(x, y) -> RotateRowRight x y)

        [(Just "rotate column"), _, _, Just column, Just amount] ->
          Just (column, amount)
            |> Maybe.andThen stringPairToInts
            |> Maybe.map (\(x, y) -> RotateColumnDown x y)

        _ -> Nothing
  in
    (find
      (AtMost 1)
      (regex "(rect|rotate row|rotate column) (?:(?:(\\d+)+x(\\d+))|(?:.=(\\d+) by (\\d+)))")
      string
    )
      |> List.head
      |> Maybe.map .submatches
      |> Maybe.andThen parseSubmatches


setPixel : Pixel -> (Int, Int) -> Grid -> Grid
setPixel pixel pos grid =
    {grid | pixels = Dict.insert pos pixel grid.pixels}


setRect : (Int, Int) -> Pixel -> Grid -> Grid
setRect (right, bottom) pixel grid =
  List.range 0 (right - 1)
  |> List.concatMap (\x -> List.map (\y -> (x, y)) (List.range 0 (bottom - 1)))
  |> List.foldl (setPixel On) grid

processInstruction: Model -> Model
processInstruction model =
  case model.instructions of
    (RectOn x y :: rest) ->
      {model | grid = setRect (x, y) On model.grid }
    _ ->
      model

stepThrough: (Model -> Model) -> Message -> Model -> (Model, Cmd Message)
stepThrough stepFunction Step model =
  (stepFunction model, Cmd.none)

update : Message -> Model -> (Model, Cmd Message)
update = stepThrough processInstruction

subscriptions model =
  every second (\t -> Step)

gridToString : Grid -> String
gridToString grid =
  let
    pixelToChar: Int -> Int -> Char
    pixelToChar row col =
      case (
        Dict.get (col, row) grid.pixels
      ) |> Maybe.withDefault Off of
        On -> '#'
        Off -> '.'

    rowToString: Int -> String
    rowToString row =
      List.range 0 (grid.width - 1)
        |> List.map (pixelToChar row)
        |> String.fromList
  in
    List.range 0 (grid.height - 1)
      |> List.map rowToString
      |> String.join "\n"

viewGrid : Grid -> Html Message
viewGrid grid =
  pre []
    [gridToString grid |> text]

view model =
    viewGrid model.grid

main =
    program { init = init, view = view, update = update, subscriptions = subscriptions }
