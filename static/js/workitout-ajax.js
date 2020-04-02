$('#success_save').hide();
$(document).ready(function() {
    var like;
    like = $("#like_start").attr('data-liked');
    if(like=="True"){
        $('#like_btn').hide();
        $('#unlike_btn').show();
    }else{
        $('#unlike_btn').hide();
        $('#like_btn').show();
        
    }
    $('#like_btn').click(function() {
        var workoutIdVar;
        var userIdVar;
        workoutIdVar = $(this).attr('data-workoutid');
        userIdVar = $(this).attr('data-userid');
        likeVar = true;
        
        $.get('/workitout/like_workout',
            {'workout_id': workoutIdVar,'user_id':userIdVar,'like':likeVar},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
                $('#unlike_btn').show();
                
             })
    });

    $('#unlike_btn').click(function() {
        var workoutIdVar;
        var userIdVar;
        workoutIdVar = $(this).attr('data-workoutid');
        userIdVar = $(this).attr('data-userid');
        likeVar = false;
        $.get('/workitout/like_workout',
            {'workout_id': workoutIdVar,'user_id':userIdVar,'like':likeVar},
            function(data) {
                $('#like_count').html(data);
                $('#unlike_btn').hide();
                $('#like_btn').show();
            })
    });

    var follow;
    follow = $("#follow_start").attr('data-isFollowing');
    if(follow=="true"){
        $('#follow_btn').hide();
        $('#unfollow_btn').show();
    }else{
        $('#unfollow_btn').hide();
        $('#follow_btn').show();
        
    }
    $('#follow_btn').click(function() {
        var followerIdVar;
        var userIdVar;
        followerIdVar = $(this).attr('data-followerid');
        userIdVar = $(this).attr('data-userid');
        toFollow = true;
        $.get('/workitout/follow_user',
            {'follower_id': followerIdVar,'user_id':userIdVar,'to_follow':toFollow},
            function(data) {
                $('#follow_count').html(data);
                $('#follow_btn').hide();
                $('#unfollow_btn').show();
                
             })
    });

    $('#unfollow_btn').click(function() {
        var followerIdVar;
        var userIdVar;
        followerIdVar = $(this).attr('data-followerid');
        userIdVar = $(this).attr('data-userid');
        toFollow = false;
        $.get('/workitout/follow_user',
            {'follower_id': followerIdVar,'user_id':userIdVar,'to_follow':toFollow},
            function(data) {
                $('#follow_count').html(data);
                $('#unfollow_btn').hide();
                $('#follow_btn').show();
                
             })
    });

   var isSaved
    isSaved = $("#like_start").attr('data-isSaved');
    if(isSaved=="True"){
        $('#save_btn').hide();
        $('#unsave_btn').show();
    }else{
        $('#unsave_btn').hide();
        $('#save_btn').show();
        
    }
    $('#save_btn').click(function() {
        var workoutIdVar;
        var userIdVar;
        workoutIdVar = $(this).attr('data-workoutid');
        userIdVar = $(this).attr('data-userid');
        toSave = "true";
        $.get('/workitout/save_workout',
            {'workout_id': workoutIdVar,'user_id':userIdVar,'to_save':toSave},
            function(data) {
                $('#success_save').html("You successfully saved "+"<b>"+data+"</b>");
                $('#save_btn').hide();
                $('#unsave_btn').show();
                $('#success_save').show();
                
             })
    });

    $('#unsave_btn').click(function() {
        var workoutIdVar;
        var userIdVar;
        workoutIdVar = $(this).attr('data-workoutid');
        userIdVar = $(this).attr('data-userid');
        toSave = "false";
        $.get('/workitout/save_workout',
            {'workout_id': workoutIdVar,'user_id':userIdVar,'to_save':toSave},
            function(data) {
                $('#success_save').html("You successfully removed "+"<b>"+data+"</b>"+" from your saved workouts");
                $('#unsave_btn').hide();
                $('#save_btn').show();
                $('#success_save').show();
                
             })
    });






});