module View exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Types exposing (..)

root: Model -> Html Msg

root model =
    case model.news of
        Loading ->
            text "Plz wait"
        Failed err ->
            text (toString err)
        Succeed newsItems ->
            div []
            [ h1 [ style [ ("font-style", "italic") ] ]
            [ text "News!" ]
            ,ul [] (List.map newsItem newsItems)
            ,div [] [
                code []
                [text (toString model)]
                ]
                ]


newsItem: News -> Html Msg
newsItem news =
    li []
    [
        h3 [] [text (news.headline)]
        ]

