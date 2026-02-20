#!/bin/bash
function_one (){
    echo "This is from the first function"
    function_two
   
}

function_two () {
    echo "This is from the second function"
    function_three
}

function_three () {
    echo "This is from the third function"
}
function_one