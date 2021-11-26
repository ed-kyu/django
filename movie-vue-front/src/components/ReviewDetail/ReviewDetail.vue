<template>
  <div class="container">
    <div v-if="review" class="pt-5">
      <!-- <h1 class="my-3">{{ this.$store.state.authUser }}의 {{ review.movie.title }} 리뷰</h1> -->
      <div class="card">
        <div class="card-header d-flex">
          <img :src="get_path(review.movie)" alt="">
        <div class="card-body">
          <!-- <p class="mx-2">{{ $route.query.reviewId }}번째 글</p> {{ movie_id }} -->
          <div class="d-flex justify-content-left align-items-center">
            <h2 class="mx-2 review-title">{{ review.title }}</h2>
            <h5 class="mx-2 review-title">by {{review.user.username}}</h5>
          </div>
          <div class="d-flex">
            <div class="mx-2  review-made">작성시각:{{ review.created_at.substring(0, 10)}} {{ review.created_at.substring(11, 16) }}</div>
            <div v-if="review.updated_at !== review.created_at" class="mx-2 review-made">수정시각:{{ review.updated_at.substring(0, 10)}} {{ review.updated_at.substring(11, 16) }}</div>
          </div>
          <hr>
          <div class="mx-2 review-content d-flex justify-content-start">{{ review.content }}</div>
          
        </div>

        
        </div>
      </div> 
      
      
      <div v-if="review && genres">
        <div v-for="genre in review.movie.genres" :key="genre.id">
          <!-- {{ genre.id }} | {{ genre.name }} -->
        </div>
        <comment-form class="mt-3" :review_json="review"></comment-form>
        <comment-list :review_json="review"></comment-list>
      </div>
    </div>

    <div class="d-flex justify-content-end align-items-center add-box mb-3">
        <div v-if="review">
          <!-- pk{{ review.id }} -->
          <span v-if="review.user === this.$store.state.authUser.id">
            <span v-if="isEditing && review.user === this.$store.state.authUser.id">
            <input required type="text" v-model="newReview.title">
            <input required type="text" v-model="newReview.content">
            <input required type='number' v-model="newReview.rate" class="mx-2" min='1' max='5' step='1'>
            <button @click="onSave" class="btn btn-sm btn-warning text-e mx-2">save</button>
            </span>
            <span v-else>
            <!-- {{ todo.title }}  -->
            <button @click="onClick" class="btn btn-sm btn-warning text-e mx-2">Edit</button>
            </span>
            <button @click="deleteReview(review.id)" class="btn btn-warning btn-sm">Delete</button>
          </span>
        </div>
      </div>
  </div>
</template>

<script>
const SERVER_URL = process.env.VUE_APP_SERVER_URL
import axios from 'axios'
import CommentForm from '@/components/ReviewDetail/CommentForm.vue'
import CommentList from '@/components/ReviewDetail/CommentList.vue'
import { mapActions } from 'vuex'

export default {
    name: 'ReviewDetail',
    data() {
      return {
        review: '',
        genres: this.$store.state.genres,
        movie_id: this.$route.query.movieId,
        review_detail: '',
        isEditing: false,
      }
    },
    components: {
      CommentForm, CommentList,
    },
    methods: {
      get_path: function(card) {
          return "https://www.themoviedb.org/t/p/w200/" + card.poster_path
      },
      getToken: function () {
        const token = localStorage.getItem('jwt')
        const config = {
          headers: {
            Authorization: `JWT ${token}`
          }
        }
        return config
      },
      getReviewDetail: function () {
        // console.log('dddddddddd', this.$route.query.reviewId)
        const config = this.getToken()
        axios.get(`${SERVER_URL}/reviews/${this.$route.query.reviewId}/detail/`, config)
          .then((res) => {
            this.review = res.data
            console.log(res)
            console.log('review:', this.review)
          })
          .catch((error) => {
            console.log(error)
          })
      },
      deleteReview: function (review_pk) {
        console.log('delete..', review_pk)
        axios({
          method: 'delete',
          url: `${SERVER_URL}/reviews/${review_pk}/`,
          headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
        })
          .then(res => {
            console.log(res)
            this.$store.dispatch('LoadAllReviews', this.$route.params.id)
            this.myReview.title = null
            this.myReview.content = null
            this.myReview.rate = 3
          })
          .catch(err => {
            console.log(err)
          })
      },
      editReview: function (review_pk) {
            console.log('edit..review', review_pk)
            axios({
            method: 'put',
            url: `${SERVER_URL}/reviews/${review_pk}/`,
            headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
            data: { // Using data from Vue
              content: this.content,
            },
            })
            .then(res => {
                console.log(res)
                this.$store.dispatch('LoadAllComments', this.$route.query.reviewId)
                this.content = ''
            })
            .catch(err => {
                console.log(err)
            })
        },
        ...mapActions([
        // 'deleteReview',
        'UpdateReview',
        ]),
        onClick() {    
            this.isEditing = !this.isEditing
        },
        onSave() {
            // console.log('save btn', comment_pk)
            this.review.title = this.newReview.title
            this.review.content = this.newReview.content
            this.review.rate = this.newReview.rate
            console.log('new Review', this.newReview)
            this.UpdateReview(this.newReview)
            this.isEditing = !this.isEditing
        }
  },
  created: function() {
    if (localStorage.getItem('jwt')) {
      this.getReviewDetail()
    } else {
      this.$router.push({name: 'Home'})
    }
  },
  computed: {
    
  }
}
</script>

<style scoped>
.review-content {
  color: black;
  font-weight: 900;
  font-size: 30px;
}
.review-title {
  color: black;
  font-weight: bold;
}
.review-made {
  font-size: 12px;
  color: gray;
}
hr {
  color: black;
}
</style>