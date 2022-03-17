function init()
{
    canvas = document.getElementById("mycanvas")
    W = canvas.width = 500;
    H = canvas.height = 500;
    pen = canvas.getContext('2d')
    pen.fillStyle = "red"
    cs = 40;
    gameover = false;
    score = 0;
    food = getRandomFood();
    snake = {
        init_len : 5,
        color :"blue",
        cells : [],
        direction : "right",
        
        createSnake:function(){
            for(var i=this.init_len;i>0;i--)
            {
                this.cells.push({x:i,y:0});
            }
        },
        drawSnake:function(){
            for(var i=0;i<this.cells.length;i++)
            {
                pen.fillStyle = this.color
                pen.fillRect(this.cells[i].x*cs,this.cells[i].y*cs,cs-3,cs-3)
             }
        },
        updateSnake:function(){
            var headX = this.cells[0].x;
            var headY = this.cells[0].y;
            if(headX==food.x && headY==food.y)
            {
                food = getRandomFood();
                score++;
            }
            else
            {
            this.cells.pop();
            }
            
            var nextX,nextY;
            if(this.direction=="right")
            {
                nextX = headX+1;
                nextY = headY
            }
            else if(this.direction=="down")
            {
                nextX = headX;
                nextY = headY+1;   
            }
            else if(this.direction=="up")
            {
                nextX = headX;
                nextY = headY-1;   
            }
            else if(this.direction=="left")
            {
                nextX = headX-1;
                nextY = headY;   
            }
            this.cells.unshift({x:nextX,y:nextY})

            var lastX = Math.round(W/cs);
            var lastY = Math.round(H/cs);

            if(this.cells[0].y<0 || this.cells[0].x<0 ||this.cells[0].y>lastY || this.cells[0].x>lastX)
            {
                gameover = true; 
            }

        }
    };
    snake.createSnake();
    function keyPressed(e)
    {
        if(e.key=="ArrowRight")
        {
            snake.direction="right"
        }
        else if(e.key=="ArrowLeft")
        {
            snake.direction="left"
        }
        else if(e.key=="ArrowUp")
        {
            snake.direction="up"
        }
        else if(e.key=="ArrowDown")
        {
            snake.direction="down"
        }
    }
    document.addEventListener("keydown",keyPressed)
}
function draw()
{
    pen.clearRect(0,0,W,H)
    // pen.fillRect(rect.x,rect.y,rect.w,rect.h)
    // pen.fillStyle = "red"
    snake.drawSnake();
    pen.fillStyle = food.color
    pen.fillRect(food.x*cs,food.y*cs,cs-3,cs-3)
    pen.fillStyle = "black"
    pen.font = "25px Roboto"
    pen.fillText(score,50,50)
    
}
function update()
{
    // rect.x+= rect.speed
    snake.updateSnake();
}
function getRandomFood()
{
    var foodX = Math.round(Math.random()*(W-cs)/cs);
    var foodY = Math.round(Math.random()*(H-cs)/cs);
    var food = 
    {
        x:foodX,
        y:foodY,
        color:"red"
    }
    return food
}
function gameloop()
{
    if(gameover==true)
    {
        clearInterval(f);
        alert("game over!");
    }
    draw();
    update();
}
init();
var f = setInterval(gameloop,100);