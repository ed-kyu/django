<template>
  <div class="d-flex mt-5 justify-content-center align-items-center">
      <div class="comment mx-5">댓글</div>
      <!-- <p>현재 로그인된 사람: {{this.$store.state.authUser.id}}</p> -->
      <input type="text"
      v-model.trim="content"
      @keyup.enter="createComment"
      style="width: 70rem; height: 7rem;"
      class="px-5"
      >
      <button @click="createComment" class="btn btn-secondary mx-1" style="height: 7rem;">입력</button>
      <hr>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
const SERVER_URL = process.env.VUE_APP_SERVER_URL
import axios from 'axios'

export default {
    name: 'CommentForm',
    data() {
      return {
        content : null,
      }
    },
    props: {
      review_json: Object,
    },
    methods: {
      createComment: function () {
      if (this.content) {
        axios({
          method: 'post',
          url: `${SERVER_URL}/reviews/${this.$route.query.reviewId}/comments/`,
          data: { // Using data from Vue
              content: this.content,
          },
          headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
        })
          .then(res => {
            console.log(res)
            this.$store.dispatch('LoadAllComments', this.$route.query.reviewId)
            this.content = ''
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    
    ...mapActions(['LoadAllComments']),
  },
  
}

</script>

<style scoped>
hr {
  color: white;
}
.comment {
  color: white;
  font-weight: bold;
}
</style>