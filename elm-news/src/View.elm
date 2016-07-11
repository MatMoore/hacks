module View exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Types exposing (..)
import CDN exposing (bootstrap)


root : Model -> Html Msg
root model =
    case model.news of
        Loading ->
            text "Plz wait"

        Failed err ->
            text (toString err)

        Succeed newsItems ->
            div []
                [ bootstrap.css
                , h1 [ style [ ( "margin-left", "0.2em" ), ( "font-style", "italic" ) ] ]
                    [ text "News!" ]
                , ul [ class "list-group" ] (List.map newsItem newsItems)
                  {- , div []
                     [ code []
                         [ text (toString model) ]
                     ]
                  -}
                ]


newsItem : News -> Html Msg
newsItem news =
    li [ class "list-group-item" ]
        [ h3 [] [ text (news.headline) ]
        ]
