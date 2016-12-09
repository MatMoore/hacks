module Test.Day08 exposing (..)

import Day08 exposing (..)
import Dict exposing (Dict)
import Test exposing (..)
import Expect exposing (Expectation, equal, all, onFail)


hasValue : Pixel -> ( Int, Int ) -> Grid -> Expectation
hasValue pixel pos grid =
    equal (getPixel pos grid) pixel
        |> onFail
            ("Expected "
                ++ (toString pos)
                ++ " to be "
                ++ (toString pixel)
                ++ "\n"
                ++ (gridToString grid)
            )


testGrid : ( Int, Int ) -> List ( Int, Int ) -> Grid
testGrid ( width, height ) onPixels =
    { width = width
    , height = height
    , pixels =
        Dict.fromList
            (onPixels |> List.map (\pos -> ( pos, On )))
    }


suite : Test
suite =
    describe "Day08"
        [ describe "Day08.rotateRowRight"
            [ test "affected row is rotated" <|
                \() ->
                    let
                        grid =
                            testGrid ( 10, 5 )
                                [ ( 0, 0 )
                                , ( 1, 0 )
                                , ( 2, 0 )
                                ]

                        rotated =
                            rotateRowRight ( 0, 3 ) grid
                    in
                        all
                            [ hasValue Off ( 0, 0 )
                            , hasValue Off ( 1, 0 )
                            , hasValue Off ( 2, 0 )
                            , hasValue On ( 3, 0 )
                            , hasValue On ( 4, 0 )
                            , hasValue On ( 5, 0 )
                            , hasValue Off ( 6, 0 )
                            , hasValue Off ( 7, 0 )
                            , hasValue Off ( 8, 0 )
                            , hasValue Off ( 9, 0 )
                            ]
                            rotated
            , test "unaffected row is unchanged" <|
                \() ->
                    let
                        grid =
                            testGrid ( 10, 5 )
                                [ ( 0, 0 )
                                , ( 1, 0 )
                                , ( 2, 0 )
                                , ( 1, 1 )
                                ]

                        rotated =
                            rotateRowRight ( 0, 3 ) grid
                    in
                        all
                            [ hasValue Off ( 0, 1 )
                            , hasValue On ( 1, 1 )
                            , hasValue Off ( 2, 1 )
                            , hasValue Off ( 3, 1 )
                            , hasValue Off ( 4, 1 )
                            , hasValue Off ( 5, 1 )
                            , hasValue Off ( 6, 1 )
                            , hasValue Off ( 7, 1 )
                            , hasValue Off ( 8, 1 )
                            , hasValue Off ( 9, 1 )
                            ]
                            rotated
            , test "rotating off the edge wraps around to the other side" <|
                \() ->
                    let
                        grid =
                            testGrid ( 10, 5 )
                                [ ( 0, 0 )
                                , ( 1, 0 )
                                , ( 2, 0 )
                                ]

                        rotated =
                            rotateRowRight ( 0, 9 ) grid
                    in
                        all
                            [ hasValue On ( 0, 0 )
                            , hasValue On ( 1, 0 )
                            , hasValue Off ( 2, 0 )
                            , hasValue Off ( 3, 0 )
                            , hasValue Off ( 4, 0 )
                            , hasValue Off ( 5, 0 )
                            , hasValue Off ( 6, 0 )
                            , hasValue Off ( 7, 0 )
                            , hasValue Off ( 8, 0 )
                            , hasValue On ( 9, 0 )
                            ]
                            rotated
            ]
        , describe "Day08.parseInstructions"
            [ test "parses all input" <|
                \() ->
                    let
                        inputLines =
                            (String.lines input)

                        parsed =
                            parseInstructions inputLines
                    in
                        equal (List.length inputLines) (List.length parsed)
            ]
        ]
