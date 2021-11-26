<template>
  <div class="container row d-flex review-box" v-if="review">
    
    <!-- <router-link :to="`/reviews?movieId=${movie_id}&reviewId=${review_pk}`" class="reviews"> -->
    <router-link :to="{ name: 'ReviewDetail', query: { movieId: this.review.movie, reviewId: this.review.id } }" class="reviews">
      <div v-if="review_rate > 0" class="review-rate d-flex my-1 align-items-center">
        <p class="my-1 stars">
          {{ review_star_render(review_rate)}}
        </p>
        <div class="mx-3 d-flex align-items-center">
          <router-link :to="{ name: 'Profile', query: {username: review.user.username, }}">
          <div class="mx-3 text-truncate">
            {{ review.user.username }} | 
          </div>
          </router-link>
          <div class="mx-3">
            {{ review.title }} 
          </div>
          <div class="mx-3">
            |
          </div>
          
        </div>
        <div class="mx-3 d-flex justify-content-center">
          <div class="mx-2 made-box">작성시각 {{ review.created_at.substring(2, 10) }}, {{ review.created_at.substring(11, 16) }}</div>
          <div v-if="review.updated_at !== review.created_at" 
          class="mx-2 made-box">수정시각 {{ review.updated_at.substring(2, 10) }}, {{ review.updated_at.substring(11, 16) }}</div>
        </div>
      </div>
    </router-link>
      <div class="d-flex justify-content-end align-items-center add-box mb-3">
        <div v-if="review">
          <!-- pk{{ review.id }} -->
          <span v-if="review.user.id === this.$store.state.authUser.id">
            <span v-if="isEditing && review.user.id === this.$store.state.authUser.id">
            <input required type="text" v-model="newReview.title">
            <input required type="text" v-model="newReview.content">
            <input required type='number' v-model="newReview.rate" class="mx-2" min='1' max='5' step='1'>
            <button @click="onSave" class="btn btn-sm btn-warning text-e mx-2">Save</button>
            </span>
            <span v-else>
            <!-- {{ todo.title }}  -->
            <button @click="onClick" class="btn btn-sm btn-warning text-e mx-2">Edit</button>
            </span>
            <button @click="deleteReview(review.id)" class="btn btn-warning btn-sm">Delete</button>
          </span>
          <span v-else>
            <div class="empty-box">

            </div>
          </span>
        </div>
      </div>
      <hr/>
  </div>
</template>

<script>
const SERVER_URL = process.env.VUE_APP_SERVER_URL
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
    name: "Review",
    props: {
        review: Object,
    },
    data() {
      return {
        movie_id : '',
        review_pk : '',
        review_title : '',
        review_rate: 5,
        newReview: { ...this.review },
        isEditing: false,
      }
    },
    methods: {
      
      // ...mapActions(['LoadAllReviews']),
      getToken: function () {
        const token = localStorage.getItem('jwt')
        const config = {
          headers: {
            Authorization: `JWT ${token}`
          }
        }
        return config
      },
      setVariable: function () {
        // console.log('test:', this.review)
        this.movie_id = this.review.movie_id
        this.review_pk = this.review.pk
        this.review_title = this.review.title
        this.review_rate = this.review.rate
      },
      review_star_render: function(num) {
        return '★'.repeat(num) + '☆'.repeat(5-num) // ⭐★
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
      this.setVariable()
    } else {
      this.$router.push({name: 'Login'})
    }
  },
}
</script>

<style scoped>
.made-box {
  font-size: 13px;
  color: gray
}
.empty-box {
  height: 31px;
}
.review-box {
  /* border: 2px solid beige; */
  /* border-radius: 10%; */
}
.reviews {
  text-decoration: none;
  color: whitesmoke;
}
hr {
  /* border: 0;
  height: 1px;
  background: red */
}
.stars {
  color: yellow;
  font-size: 20px;
}
/* .add-box {
  position: relative;
  top: -30px;
} */
</style>