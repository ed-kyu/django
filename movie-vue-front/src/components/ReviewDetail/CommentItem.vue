<template>
  <div class="d-flex justify-content-start align-items-center my-3 mx-2 comment-box">
      <div class="d-flex align-items-center mx-3">
        <div class="mx-2 my-comment" v-if="comment.user.id === this.$store.state.authUser.id">
            <p class="my-comment-name">ID: {{ comment.user.username }}</p>
            <p class="my-comment-content">{{ comment.content }}</p>
        </div>
        <div v-else class="comment">
            <p class="other-comment-name">ID: {{ comment.user.username }}</p>
            <p class="other-comment-content">{{ comment.content }}</p>
        </div>
        <div class="time-box d-flex">
            <!-- {{comment}} -->
        <div class="mx-2 comment-made">{{ comment.created_at.substring(2, 10)}} {{ comment.created_at.substring(11, 16) }}</div>
        <!-- v-if="comment.updated_at !== comment.created_at"  -->
        <div class="mx-2 comment-made">수정시각: {{ comment.updated_at.substring(2, 10)}} {{ comment.updated_at.substring(11, 16) }}</div>
        </div>
      </div>
    <div>
        <div class="edit-box d-flex align-items-center" v-if="comment.user.id === this.$store.state.authUser.id">
            <div v-if="isEditing">
            <input type="text" v-model="newComment.content" @keypress.enter="onSave">
            <button @click="onSave" class="btn btn-sm btn-warning text-e mx-2">save</button>
            </div>
            <div v-else>
            <button @click="onClick" class="btn edit-btn btn-sm btn-warning text-e mx-2">edit</button>
            </div>
            <button class="btn delete-btn text-e text-white" @click="deleteComment(comment.id)">X</button>
        </div>
    
    </div>
  </div>
</template>

<script>
const SERVER_URL = process.env.VUE_APP_SERVER_URL
import axios from 'axios'
import { mapActions } from 'vuex'

export default {
    name: 'CommentItem',
    props: {
        comment: Object,
    },
    data(){
        return {
            user : this.$store.state.authUser.id,
            newComment: { ...this.comment },
            isEditing: false,
        }
    },
    methods: {
        deleteComment: function (comment_pk) {
            console.log('delete..commentt', comment_pk)
            axios({
            method: 'delete',
            url: `${SERVER_URL}/reviews/comments/${comment_pk}/`,
            headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`}
            })
            .then(res => {
                console.log(res)
                this.$store.dispatch('LoadAllComments', this.$route.query.reviewId)
                this.myReview.title = null
                this.myReview.content = null
                this.myReview.rate = 3
            })
            .catch(err => {
                console.log(err)
            })
        },
        editComment: function (comment_pk) {
            console.log('edit..comment', comment_pk)
            axios({
            method: 'put',
            url: `${SERVER_URL}/reviews/comments/${comment_pk}/`,
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
        ...mapActions(['UpdateComment']),
        onClick() {    
            this.isEditing = !this.isEditing
        },
        onSave() {
            // console.log('save btn', comment_pk)
            this.comment.content = this.newComment.content
            console.log('new Comment', this.newComment)
            this.UpdateComment(this.newComment)
            this.isEditing = !this.isEditing
        }
    }
}
</script>

<style>
.delete-btn {
    font-size: 25px;
}
.edit-btn {
    border-radius: 25%;
}
.comment {
  color: white;
  font-weight: bold;
  font-size: 17px;
}
.my-comment {
  color: royalblue;
  font-weight: bold;
  font-size: 17px;
}
.comment-made {
  color: gray;
  font-size: 15px;
}
.comment-box {
  border: 1px solid gray;
  height: 8rem;
  position: relative;
  border-radius: 10px;
  /* margin-right: 140px; */
}
.time-box {
  position: absolute;
  top: 10px;
  left: 130px;
}
.my-comment-name {
  position: absolute;
  top: 10px;
  left: 20px;
}
.my-comment-content {
  position: absolute;
  top: 50px;
  left: 20px;
  /* right: 20px; */
}
.other-comment-name {
  position: absolute;
  top: 10px;
  left: 20px;
  /* right: 20px; */
}
.other-comment-content {
  position: absolute;
  top: 50px;
  left: 20px;
}
.edit-box {
  position: absolute;
  right: 10px;
  top: 5px;
}
</style>