function [new_pos_right, new_pos_left] = center_attack(pos_right, pos_left,General,Hannibal)
   
    
    c=0.94;
    random_vector_right = randn(size(pos_right)) * c*rand;
    random_vector_left = randn(size(pos_left)) * c*rand;
    new_pos_right = pos_right + random_vector_right.*(General - pos_right) ;
    new_pos_left = pos_left + random_vector_left.*(Hannibal - pos_left) ;
    
    
    
%     new_pos_right = parallaxe(new_pos_right,Hannibal) ; 
%     new_pos_left = parallaxe(new_pos_left,General) ;



end
