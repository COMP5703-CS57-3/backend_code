import giftdata from "../../data/giftlist.json";
import React,{useState} from "react";
import ReactDOM from "react-dom";
import GiftDetail from "./GiftDetail";
import WishProvider from "../../tools/useWish";
import WishDetail from "./WishListDetail";

export default function WishListContentProvider(){
    return(
        <WishProvider login="test">
            <WishDetail/>
        </WishProvider>
    )
}