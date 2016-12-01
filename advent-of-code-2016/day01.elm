module Day01 exposing (..)

import Html exposing (..)
import Dict exposing (..)


input =
    "R1, L3, R5, R5, R5, L4, R5, R1, R2, L1, L1, R5, R1, L3, L5, L2, R4, L1, R4, R5, L3, R5, L1, R3, L5, R1, L2, R1, L5, L1, R1, R4, R1, L1, L3, R3, R5, L3, R4, L4, R5, L5, L1, L2, R4, R3, R3, L185, R3, R4, L5, L4, R48, R1, R2, L1, R1, L4, L4, R77, R5, L2, R192, R2, R5, L4, L5, L3, R2, L4, R1, L5, R5, R4, R1, R2, L3, R4, R4, L2, L4, L3, R5, R4, L2, L1, L3, R1, R5, R5, R2, L5, L2, L3, L4, R2, R1, L4, L1, R1, R5, R3, R3, R4, L1, L4, R1, L2, R3, L3, L2, L1, L2, L2, L1, L2, R3, R1, L4, R1, L1, L4, R1, L2, L5, R3, L5, L2, L2, L3, R1, L4, R1, R1, R2, L1, L4, L4, R2, R2, R2, R2, R5, R1, L1, L4, L5, R2, R4, L3, L5, R2, R3, L4, L1, R2, R3, R5, L2, L3, R3, R1, R3"


type Rotation
    = Left
    | Right


type Instruction
    = Rotate Rotation
    | Forward


type Direction
    = North
    | South
    | East
    | West


type alias Location =
    { north : Int, east : Int }


type alias Step =
    { location : Location
    , direction : Direction
    , visitCount : Dict ( Int, Int ) Int
    }


locationKey location =
    ( location.north, location.east )


start : Step
start =
    { location = { north = 0, east = 0 }, direction = North, visitCount = Dict.singleton ( 0, 0 ) 1 }


instructions : List Instruction
instructions =
    String.split ", " input
        |> List.concatMap parseCommand


parseBlocks digit =
    case String.toInt digit |> Result.toMaybe of
        Just integer ->
            List.repeat integer Forward

        _ ->
            []


parseRotation rotation =
    case rotation of
        'L' ->
            Just (Rotate Left)

        'R' ->
            Just (Rotate Right)

        _ ->
            Nothing


parseCommand : String -> List Instruction
parseCommand str =
    case String.uncons str of
        Just ( rotation, blocks ) ->
            case parseRotation rotation of
                Just instruction ->
                    instruction :: (parseBlocks blocks)

                _ ->
                    []

        _ ->
            []


turn : Rotation -> Direction -> Direction
turn rotation start =
    case ( rotation, start ) of
        ( Left, North ) ->
            West

        ( Left, East ) ->
            North

        ( Left, South ) ->
            East

        ( Left, West ) ->
            South

        ( Right, North ) ->
            East

        ( Right, East ) ->
            South

        ( Right, South ) ->
            West

        ( Right, West ) ->
            North


forward : Direction -> Location -> Location
forward direction start =
    case direction of
        North ->
            { start | north = start.north + 1 }

        East ->
            { start | east = start.east + 1 }

        South ->
            { start | north = start.north - 1 }

        West ->
            { start | east = start.east - 1 }


move : Instruction -> Step -> Step
move instruction step =
    case instruction of
        Rotate rotation ->
            { step | direction = turn rotation step.direction }

        Forward ->
            let
                translated =
                    { step | location = forward step.direction step.location }

                countLocation prev =
                    case prev of
                        Just count ->
                            Just (count + 1)

                        Nothing ->
                            Just 1
            in
                { translated | visitCount = Dict.update (locationKey translated.location) countLocation translated.visitCount }


compute : List Step
compute =
    List.scanl move start instructions


blocksAway : Location -> Int
blocksAway location =
    (abs location.north) + (abs location.east)


main =
    Html.beginnerProgram { model = compute, view = view, update = update }


update msg model =
    model


resultString step =
    let
        numberOfVisits =
            Dict.get (locationKey step.location) step.visitCount
                |> Maybe.withDefault 1
    in
        (toString step.location)
            ++ " facing "
            ++ (toString step.direction)
            ++ ", visited "
            ++ (toString numberOfVisits)
            ++ " times. This is "
            ++ (toString (blocksAway step.location))
            ++ " blocks away"


view steps =
    let
        wrapText node =
            p [] [ node ]

        paragraphs =
            steps
                |> List.map resultString
                |> List.map text
                |> List.map wrapText
    in
        div []
            paragraphs
