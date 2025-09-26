function [new_pos_right, new_pos_left] = left_attack(pos_right, pos_left, General, Hannibal)
 random_vector_right = randn(size(pos_right)) * 0.5;
    random_vector_left = randn(size(pos_left)) * 0.5;
    % Mirror positions
    new_pos_right = 2*mean(pos_left) - random_vector_right.*pos_right;
    new_pos_left = 2*mean(pos_right) - random_vector_left.*pos_left;

  new_pos_right =  0.94*parallaxe(new_pos_right,Hannibal) ; 
  new_pos_left =  0.94*parallaxe(new_pos_left,General) ;
end
