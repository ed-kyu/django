<template>
  <div class="mt-3">
    <div> <!--@submit.prevent="onClick()"-->
      <div class="container">
          <div class="d-flex justify-content-center align-items-center">
              
              <div class="text-center" align="center">리뷰 제목</div>
              <input required class="mx-2" type="text" v-model.trim="myReview.title" style="height:2.5rem; width: 50rem;">
          </div>
          <div class="d-flex justify-content-center align-items-center">
              <div class="text-center" align="center">리뷰 내용</div>
              <textarea required @keyup.enter="creteReview" class="mx-2" type="text" v-model.trim="myReview.content" style="height:5rem; width: 50rem;">
              </textarea>
          </div>
          <div class="d-flex justify-content-center align-items-center">
              
          </div>
          <div class="d-flex justify-content-end align-items-center mx-2 my-2 add-btn">
            <div class="">
              아이디 | {{ $store.state.authUser.username }}
            </div>
            <div class="d-flex">
                <select class="form-select mx-2" name="rates" id="rates" v-model="myReview.rate">
                  <optgroup label="평점">
                  <option value="1">⭐</option>
                  <option value="2">⭐⭐</option>
                  <option value="3">⭐⭐⭐</option>
                  <option value="4">⭐⭐⭐⭐</option>
                  <option value="5">⭐⭐⭐⭐⭐</option>
                  </optgroup>
                </select>
                <!-- <input required type='number' class="mx-2" min='1' max='5' step='1' v-model="myReview.rate"> -->
                <button @click="creteReview" class="btn btn-secondary btn-sm">Add</button> 
            </div>
          </div>
      </div>  
    </div>
  </div>
</template>

<script>
// import { mapActions } from 'vuex'
const SERVER_URL = process.env.VUE_APP_SERVER_URL
import axios from 'axios'
// import { mapActions } from 'vuex'
// import { mapState } from 'vuex'

export default {
  name: 'ReviewForm',
  data() {
    return {
      myReview: {
          title: '',
          content: '',
          rate: 3,
      },
    }
  },
  props: {
      movie_json: Object,
  },
  methods: {
    creteReview: function () {
      const myReview = {
        title: this.myReview.title,
        content: this.myReview.content,
        rate: this.myReview.rate
      }
      if (myReview.title) {
        axios({
          method: 'post',
          url: `${SERVER_URL}/reviews/movies/${this.$route.params.id}/`,
          data: { // Using data from Vue
              title: this.myReview.title,
              content: this.myReview.content,
              rate: this.myReview.rate
          },
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
      }
    },
    // onClick() {
    //   // commit('ADD_MY_REVIEW', review)
    //   axios({
    //     method: 'post',
    //     url: `${SERVER_URL}/reviews/movies/${this.$route.params.id}/create`,
    //     data: { // Using data from Vue
    //         title: this.myReview.title,
    //         content: this.myReview.content,
    //         rate: this.myReview.rate
    //     },
    //     headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
    //   })
    //     .then((res) => {
    //       console.log('send review:', res)
    //       this.myReview.title = ''
    //       this.myReview.content = ''
    //       this.myReview.rate = 3
    //       // this.LoadAllReviews(this.$route.params.id)
    //       this.$store.state.allReview.push(res)
    //     })
    //     .catch(err => {
    //       console.log(err)
    //     })
    // },
  },
}
</script>

<style scoped>
.add-btn {
  position: relative;
  right: 100px;
}
</style>