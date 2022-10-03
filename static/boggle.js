class Boggle {
    constructor() {
        this.remainingTime = 10;
        this.score = 0;
        this.words = new Array();

        this.gameHandler = setInterval(this.updateGame.bind(this), 1000);
        $(".submit-word").on("submit", this.handleSubmit.bind(this));
    }

    updateScore() {
        $(".score").text(this.score);
    }

    updateWords() {
        const $words = $(".words");
        $words.empty();
        for(const word of this.words) {
            $words.append($(`<li>${word}</li>`))
        }
    }

    updateMessage(message) {
        $('.message-box').text(message);
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        let word = $(".word").val();
        if(!word) {
            this.updateMessage("Word was not submitted")
            return;
        }

        if(this.words.includes(word)) {
            this.updateMessage("Word was already submitted")
            return;
        }

        if(this.remainingTime <= 0) {
            this.updateMessage("Time is already up!")
            return;
        }

        const response = await axios.get('/check-word', {params: {word: word}});
        if(response.data.result === 'not-word') {
            this.updateMessage(`${word} is not a word`);
        } else if (response.data.result === "not-on-board") {
            this.updateMessage('Word is not on the board')
        } else {
            this.score += word.length;
            this.words.push(word);
            this.updateScore();
            this.updateWords();
            this.updateMessage(`${word} was added for ${word.length} points!`)
        }

        $('.word').val("");
    }

    async updateGame() {
        this.remainingTime -= 1;
        $('.time').text(this.remainingTime);
        if(this.remainingTime <= 0) {
            clearInterval(this.gameHandler);
            await this.endGame();
        }
    }

    async endGame() {
        $('.submit-word').hide()
        const response = await axios.post('/post-score', {score: this.score});
        if(response.data.newRecord) {
            this.updateMessage(`Game ended! New record achieved: ${this.score}`);
        } else {
            this.updateMessage(`Game ended! Final score: ${this.score}`);
        }
    }
}

let game = null
$(document).ready(() => { game = new Boggle() })