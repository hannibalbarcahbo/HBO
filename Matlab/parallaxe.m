function [modified_pos_right] = parallaxe(pos_right,Rom_Gen)

N = size(pos_right,1);
if mod(N,2) ~= 0
 % Ensure that the number of elements in X matches the reshaping dimensions
%    assert(size(X,1) * size(X,2) == N*2, 'Number of elements in X does not match reshaping dimensions');
    couples = reshape(randperm(N-1), [], 2); % Use [] to automatically calculate size
else
    couples = reshape(randperm(N), [], 2); % Use [] to automatically calculate size
end

%couples = couples (1:floor(N/2), : ) ; 

modified_pos_right=pos_right;

modified_indices = [];

for idx = 1:size(couples, 1)
    couple_center = (pos_right(couples(idx, 1), :) + pos_right(couples(idx, 2), :)) / 2;
    center_to_gen_dist = norm(couple_center - Rom_Gen(1, :));
    
    for j = 1:2
        warrior_index = couples(idx, j);
        warrior = pos_right(couples(idx, j), :);
        influence_direction = (Rom_Gen(1, :) - warrior) / norm(Rom_Gen(1, :) - warrior);
        adjusted_step_size = center_to_gen_dist * (0.5+rand()*2);
        modified_pos_right(couples(idx, j), :) = warrior + adjusted_step_size * influence_direction;
        modified_indices = [modified_indices, warrior_index];
    end
end


% for j = 1:length(modified_indices)
%     i= modified_indices(j);
%     old_fitness = fobj(pos_right(i,:));
%     new_fitness = fobj(modified_pos_right(i,:));
%     
%     
%     if (new_fitness < old_fitness)
%         pos_right(i,:) =modified_pos_right(i,:)   ;
%         
%     end
%     
%     
%     
% end

end 
