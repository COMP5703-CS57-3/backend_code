import * as React from 'react';
import Box from '@mui/material/Box';
import Button from "@mui/material/Button";
import {useNavigate} from "react-router-dom";
import {ImageListItem, ImageListItemBar} from "@mui/material";

export default function GiftItem({id,gift_name,gift_price,gift_category,gift_side_category1,gift_side_category2,gift_discount_price,gift_cover_url}) {
    let navigate = useNavigate();
    const nav =()=> navigate("/gift/"+id);
  return (
    <Box
        sx={{
            bgcolor: 'background.paper',
            // overflow: 'hidden',
            borderRadius: '20px',
            boxShadow: 1,
            fontWeight: 'bold',
            width:280
        }}
    >
        <ImageListItem >
            <Box
                component="img"
                sx={{
                    mx: 2,
                    mt: 3,
                    height: 350,
                    width: 350,
                    maxHeight: { xs: 250, md: 300 },
                    maxWidth: { xs: 350, sm:300,md: 250 },
                    alignItems: 'center',
                    boxShadow: 2
                }}
                alt="pic"
                src= {gift_cover_url}
            />
            <ImageListItemBar
                title={<Box style={{ textAlign: "center"}}>{gift_name}</Box>}
                subtitle={
                    <Box style={{ textAlign: "center"}}>
                        <p>{gift_category},{gift_side_category1},{gift_side_category2}</p>
                        <Box sx={{fontSize:25}}>${gift_discount_price}</Box>
                                </Box>
                        }
                        position="below"
                    />
                    {/*<ImageListItemBar*/}
                    {/*    title={<Box style={{ textAlign: "center"}}>${gift.gift_discount_price}</Box>}*/}
                    {/*    position="below"*/}
                    {/*/>*/}
                    <Button  onClick={nav}>Learn More</Button>
                </ImageListItem>
        </Box>
  );
}