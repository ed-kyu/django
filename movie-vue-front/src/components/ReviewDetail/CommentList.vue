<template>
  <div v-if="allComments" class="d-flex flex-column my-3">
      <comment-item
      v-for="comment in allComments" :key="comment.id" :comment="comment"
      >
      </comment-item>
  </div>
</template>

<script>
import CommentItem from '@/components/ReviewDetail/CommentItem.vue'
// const SERVER_URL = process.env.VUE_APP_SERVER_URL
// import axios from 'axios'
import { mapState } from 'vuex'

export default {
    name: 'CommentList',
    components: {
        CommentItem,
    },
    data() {
        return {
            comments: null,
        }
    },
    props: {
      review_json: Object,
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
    },
  created: function () {
    if (localStorage.getItem('jwt')) {
    //   this.getMovieReviews()
      this.$store.dispatch('LoadAllComments', this.$route.query.reviewId)
    } else {
      this.$router.push({name: 'Login'})
    }
  },
    computed: {
    ...mapState([
      'allComments'
    ]),
  },
}
</script>

<style>

</style>