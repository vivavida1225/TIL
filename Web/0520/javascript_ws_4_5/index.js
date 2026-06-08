let count1 = 0
let count2 = 0

const playGame = function (player1, player2) {
    // 비긴 것부터 처리
    if (player1 === player2) {
        return 0
    }
    else if (player1 === 'scissors') {
        if (player2 === 'rock') {
            count2 += 1
            return 2
        } else if (player2 === 'paper') {
            count1 += 1
            return 1
        }
    } else if (player1 === 'rock') {
        if (player2 === 'scissors') {
            count1 += 1
            return 1
        } else if (player2 === 'paper') {
            count2 += 1
            return 2
        }
    } else if (player1 === 'paper') {
        if (player2 === 'rock') {
            count1 += 1
            return 1
        } else if (player2 === 'scissors') {
            count2 += 1
            return 2
        }
    }
}

const buttonClickHandler = function (event, choice) {
    console.log(choice)
    const player1 = choice
    player1Image.src = `./img/${player1}.png` //p1 이미지 변경
    // 버튼 비활성화
    const buttons = [scissorsButton, rockButton, paperButton]
    for (const btn of buttons) {
        btn.disabled = true
    }
    // player2 선택 결정 로직
    let shuffleCount = 0
    let shuffleTimerId = null

    const player2Shuffle = function () {
        const randomIndex = Math.floor(Math.random() * 3) // 0부터 3 사이의 어떤 수 생성 후 floor
        const player2Options = ['rock', 'paper', 'scissors']
        const player2 = player2Options[randomIndex]
        player2Image.src = `./img/${player2}.png` //p2 이미지 변경
        // console.log(player2)

        // player2 이미지 셔플링
        shuffleCount++ // 함수 실행마다 카운트 +1
        if (shuffleCount === 6) {
            clearInterval(shuffleTimerId)

            const gameResult = playGame(player1, player2)
            // console.log(gameResult)

            setTimeout(() => {
                // 계산된 내부 점수를 점수판에 갱신
                countAEl.textContent = count1
                countBEl.textContent = count2

                // 모달 결과 텍스트 설정
                let resultMessage = ''
                if (gameResult === 0) resultMessage = 'Tie!'
                else if (gameResult === 1) resultMessage = 'Player 1 wins!'
                else if (gameResult === 2) resultMessage = 'Player 2 wins!'

                // 모달 화면에 띄우기
                modalContent.textContent = resultMessage
                modal.style.display = 'flex'

                // 재활성화
                for (const btn of buttons) {
                    btn.disabled = false
                }
            }, 1000) 

        }
    }

    shuffleTimerId = setInterval(player2Shuffle, 50)

    

    
    
}

const scissorsButton = document.querySelector('#scissors-button')
const rockButton = document.querySelector('#rock-button')
const paperButton = document.querySelector('#paper-button')

const player1Image = document.querySelector('#player1-img')
const player2Image = document.querySelector('#player2-img')

const modal = document.querySelector('.modal')
const modalContent = document.querySelector('.modal-content')

const countAEl = document.querySelector('.countA')
const countBEl = document.querySelector('.countB')

scissorsButton.addEventListener('click', (event) => buttonClickHandler(event, 'scissors'))
rockButton.addEventListener('click', (event) => buttonClickHandler(event, 'rock'))
paperButton.addEventListener('click', (event) => buttonClickHandler(event, 'paper'))

// 모달창 닫기
modal.addEventListener('click', function () {
    modal.style.display = 'none'
})