function [new_pos_right, new_pos_left] = right_attack(pos_right, pos_left,General,Hannibal)
    reflection_plane = (mean(pos_right) + mean(pos_left)) / 2;
    random_vector_right = randn(size(pos_right)) * 0.5;
    random_vector_left = randn(size(pos_left)) * 0.5;
    new_pos_right = reflection_plane + random_vector_right.*(reflection_plane - pos_right); 
    new_pos_left = reflection_plane + random_vector_left.*(reflection_plane - pos_left) ;
    
     new_pos_right = 0.94*parallaxe(new_pos_right,Hannibal) ; 
  new_pos_left = 0.94* parallaxe(new_pos_left,General) ;
end
