<template>
  <div class="container pt-1 justify-content-center" v-if="movie_detail">
    <h1 class="my-4">{{movie_detail.title}} ({{ movie_detail.release_date.substring(0, 4) }})</h1>
    <div class="container" style="width: 70rem;">
      <div class="card movieCard text-white bg-dark">
        <!-- <img :src="get_path(movie_json)" alt="moviedetail" class="movieImage m-3"> -->
        <div class="video-container" @mouseover="mouseHoverPlay" @mouseout="mouseOutPause">
          <iframe id="movie-trailer" :src="trailer_src" frameborder="0"></iframe>
        </div>
        <div class="card-body">
          <div class="d-flex justify-content-center align-items-center">

            <div class="btn btn-warning col-1 like" @click="like" >👍 {{ likes }}</div>
            <div class="btn btn-secondary col-1 mx-3 dislike" @click="dislike" >👎{{ dislikes }}</div>
            <div class="my-rate my-star" v-if="this.myRate">
              
              {{ this.review_star_render(rate.rate) }}
              <button @click="deleteRate(rate.id)" class="btn btn-warning btn-sm">평점 삭제</button>
            </div>
          </div>

          
          <div class="card-text detail">
            <div class="d-flex justify-content-end">
              <p class="mx-2 overview"></p> |
              <p class="mx-3 overview">{{ movie_detail.runtime }}분</p> |
              <p class="mx-3 overview">★{{ movie_detail.vote_average }}</p> |
              <!-- <p class="mx-2 overview">출연: 배우 이름</p> | -->
              <p class="mx-1 overview"></p>
              <p class="mx-1 overview" v-for="genre in genres_list" :key=genre.id>
                {{genre[0].name}}
              </p>
            </div>
            <p>{{ movie_detail.overview }}</p>
          </div>
          
          <div class="card-footer">
            
            <!-- <my-review-form :movie_json="movie_detail"></my-review-form> -->
            
          </div>
        </div>
      </div>
      <review-form :movie_json="movie_detail"></review-form>
      <hr/>
      <review-list class="review-list" :movie_json="movie_detail"></review-list>
    </div>
  </div>
</template>

<script>
const YOUTUBE_KEY = process.env.VUE_APP_YOUTUBE_KEY
const SERVER_URL = process.env.VUE_APP_SERVER_URL
const API_URL = 'https://www.googleapis.com/youtube/v3/search'
import axios from 'axios'
import ReviewList from '@/components/ReviewList.vue'
import ReviewForm from '@/components/ReviewForm.vue'
import { mapActions, mapState } from 'vuex'
export default {
    name: "MovieDetail",
    components: {
      ReviewList,
      ReviewForm,
    },
    data() {
      return {
        movie_json : {}, //this.$store.state.movieCards[this.$route.params.id],
        movie_trailer_key : '',
        movie_detail: '',
        trailer_src: '',
        likes: '',
        dislikes: '',
        myRate: null,
        isNotScored: true,
        // isEditing: false,
        movie_genres: [],
      }
    },
    methods: {
      getToken: function () {
        const token = localStorage.getItem('jwt')
        const config = {
          headers: {
            Authorization: `JWT ${token}`
          }
        }
        return config
      },
      review_star_render: function(num) {
        return '⭐'.repeat(num) //+ '☆'.repeat(5-num) // ⭐★
      },
      
      getMovieDetail: function () {
        const config = this.getToken()
        axios.get(`${SERVER_URL}/movies/detail/${this.$route.params.id}/`, config)
          .then((res) => {
            this.movie_detail = res.data
            this.likes = res.data.loved
            this.dislikes = res.data.hated
            console.log('detail:', this.movie_detail)
            this.loadMovieTrailer()
          })
          .catch((error) => {
            console.log(error)
          })
      },
      like: function () {
        axios({
          method: 'POST',
          url: `${SERVER_URL}/movies/detail/${this.movie_detail.id}/like/`,
          headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
        })
        .then(res => {
          console.log(res.data)
          this.likes = res.data.likesReceived
        })
        .catch(err => {
          console.log(err)
        })
      },
      dislike: function () {
        axios({
          method: 'POST',
          url: `${SERVER_URL}/movies/detail/${this.movie_detail.id}/dislike/`,
          headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
        })
        .then(res => {
          console.log(res.data)
          this.dislikes = res.data.dislikesReceived
        })
        .catch(err => {
          console.log(err)
        })
      },
      get_path: function(card) {
          return "https://www.themoviedb.org/t/p/w200/" + card.poster_path
      },
      get_trailer_path: function(key) {
          return "https://www.youtube.com/embed/" + key
      },
      loadMovieTrailer: function() {
        setTimeout(1)
        console.log('trailerloading...',this.movie_detail.title, this.movie_detail.release_date.substring(0, 4))
        const params = {
          key: YOUTUBE_KEY,
          part: 'snippet',
          type: 'video',
          maxResults: 1,
          q: JSON.stringify(this.movie_detail.title + ' trailer ' + this.movie_detail.release_date.substring(0, 4))
        }
        axios({
          url: API_URL,
          method: 'get',
          params,
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
        })
          // .then(res=>res.json())
          .then(res => {
            console.log('..',res)
            this.movie_trailer_key = res.data.items[0].id.videoId
            this.trailer_src = this.get_trailer_path(this.movie_trailer_key)
            console.log('hmm', this.trailer_src)
          })
          .catch(err => {
            console.log(err)
          })
      },
      mouseHoverPlay: function () {
        this.trailer_src = "https://www.youtube.com/embed/" + this.movie_trailer_key + "?autoplay=1&mute=1"//"?enablejsapi=1&version=3"
        console.log("mousein", this.trailer_src)
      },
      mouseOutPause: function () {
        this.trailer_src = "https://www.youtube.com/embed/" + this.movie_trailer_key
        console.log("mouseout", this.trailer_src)
      },
      creteRate: function () {
        const rate_num = document.getElementById('rates').value
        console.log('rate clicked', rate_num)
        this.rate = rate_num
        if (this.rate) {
          axios({
            method: 'post',
            url: `${SERVER_URL}/reviews/movies/${this.$route.params.id}/createrate/`,
            data: { // Using data from Vue
                user: this.$store.state.authUser.id,
                rate: this.rate,
                movie: this.$route.params.id,
            },
            headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
          })
            .then(res => {
              console.log(res)
              this.rate = res.data
              // this.$store.dispatch('LoadAllRates', this.$route.params.id)
              this.isNotScored = false
            })
            .catch(err => {
              console.log(err)
            })
          }
        },
      deleteRate: function (rate_pk) {
        console.log('delete..rate', rate_pk)
        axios({
          method: 'delete',
          url: `${SERVER_URL}/reviews/rates/${rate_pk}/`,
          // data: { // Using data from Vue
          //     user: this.$store.state.authUser.id,
          //     movie: this.$route.params.id,
          // },
          headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
        })
          .then(res => {
            console.log(res)
            this.$store.dispatch('LoadRate', this.$route.params.id)
            this.isNotScored = true
            // this.rate.rate = 1
            this.rate.rate = ''
          })
          .catch(err => {
            console.log(err)
          })
      },
      setVariable: function () {
        // console.log('test:', this.review)
        this.myRate = this.rate.rate
      },
      changeGenre: function() {
        const genre_num = this.$store.state.genres.length
        console.log('genres',this.$store.state.genres.length)
        for (let i=0; i < genre_num; i++) {
          console.log(this.$store.state.genres[i].name)
          for(let j=0; j < this.movie_detail.genres.length; j++){
            console.log(this.movie_detail.genres[j])
            if(this.$store.state.genres[i].id === this.movie_detail.genres[j]){
              this.movie_genres.push(this.$store.state.genres[i].name)
            }

          }
        }
      },
      ...mapActions([
        'UpdateRate',
        ]),
      ...mapActions(['FetchReviews', 'LoadRate']),
  },
  computed: {
    ...mapState([
      'rate', 'genres'
    ]),
    genres_list: function() {
      const movie_genres = []
      for (let i=0; i< this.test.length; i++) {
        console.log(this.test[i])
        movie_genres.push(this.$store.state.genres.filter(idx => idx.id == this.test[i]))
      }
      return movie_genres
    },
    test: function() {
      return this.movie_detail.genres
    }
  },
  created: function() {
    if (localStorage.getItem('jwt')) {
      // this.setVariable()
      this.getMovieDetail()
      
      // console.log('whywhy..')
      // this.$store.dispatch('LoadRate', this.$route.params.id)
      // console.log('rate', this.myRate)
      // if (this.rate) this.isNotScored = true
      this.FetchReviews()
    } else {
      this.$router.push({name: 'Home'})
    }
  },

}
</script>

<style scoped>
.like {
  width: 50px;
}

.dislike {
  width: 50px;
}
.movieImage {
  width: 12rem;
}

.detail {
  margin-top: 20px;
  padding: 20px;
  border: solid 1px lightgray;
  border-radius: 10px;
}

.video-detail {
  width: 70%;           /* Detail, List를 전체 가로 비율 대비 7:3으로 설정 */
  padding-right: 1rem;  /* Detail과 List 사이의 margin */
}

.video-container {
  position: relative;   /* iframe을 container를 기준으로 위치를 지정 */
  padding-top: 56.25%;  /* 유튜브 비디오 비율을 맞추기 위한 높이 설정 */
}

.video-container > iframe {
  position: absolute;   /* container를 기준으로 위치를 지정*/
  top: 0;               /* container의 가장 위쪽으로 위치를 지정 */
  left: 0;
  width: 100%;
  height: 100%;
}

.video-container:hover {
  cursor: pointer;  
}

#movie-trailer {
  border: 4px solid #000;
  -moz-border-radius: 15px;
  border-radius: 15px;
  overflow: hidden;
}

.rate-box {
  position: absolute;
  left: 20px;
}

.card-body {
  position: relative;
}

.my-star{
  position: absolute;
  right: 20px;
}

.overview {
  font-weight: bold;
}
</style>