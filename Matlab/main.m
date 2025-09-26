%___________________________________________________________________%
%  Hannibal Barca Optimizer (HBO)              %
%                                                                   %
                                 %
%                                                                   %
%  Author and programmer: Ghaith Manita, Mohamed Wajdi Ouertani,
%                         Ouajdi Korbaa                        %
%                                                                   %
%         e-Mail: Ghaith.manita@fst.utm.tn                          %
%                 mohamed.wajdi.ouertani@gmail.com 
%                   Ouajdi.Korbaa@uso.rnu.tn            %
%                                                                   %
%               %
%                                                                   %
%   Main paper: M.W. Ouertani, G. Manita, O. Korbaa             %
%               Hannibal Barca optimizer: the power of the pincer
%               movement for global optimization and multilevel 
%               image thresholding, Cluster Computing        %
%              ,                                %
%               DOI: 10.1007/s10586-025-05134-1               %
%                                                                   %
%___________________________________________________________________%

% You can simply define your cost in a seperate file and load its handle to fobj 
% The initial parameters that you need are:
%__________________________________________
% fobj = @YourCostFunction
% dim = number of your variables
% Max_iteration = maximum number of generations
% SearchAgents_no = number of search agents
% lb=[lb1,lb2,...,lbn] where lbn is the lower bound of variable n
% ub=[ub1,ub2,...,ubn] where ubn is the upper bound of variable n
% If all the variables have equal lower bound you can just
% define lb and ub as two single number numbers

% To run HBO: [Best_score,Best_pos,HBO_cg_curve]=HBO(SearchAgents_no,Max_iteration,lb,ub,dim,fobj)
%__________________________________________

clear all 
clc

warriors_no=30; % Number of search agents

Function_name='F18'; % Name of the test function that can be from F1 to F23 (Table 1,2,3 in the paper)

Max_iteration=1000; % Maximum numbef of iterations

% Load details of the selected benchmark function
[lb,ub,dim,fobj]=Get_Functions_details(Function_name);

[Best_score,Best_pos,HBO_cg_curve]=HBO(warriors_no,Max_iteration,lb,ub,dim,fobj);
figure('Position',[500 500 660 290])
%Draw search space
subplot(1,2,1);
func_plot(Function_name);
title('Parameter space')
xlabel('x_1');
ylabel('x_2');
zlabel([Function_name,'( x_1 , x_2 )'])

%Draw objective space
subplot(1,2,2);
semilogy(HBO_cg_curve,'Color','r')
title('Objective space')
xlabel('Iteration');
ylabel('Best score obtained so far');

axis tight
grid on
box on
legend('HBO')

display(['The best solution obtained by HBO is : ', num2str(Best_pos)]);
display(['The best optimal value of the objective funciton found by HBO is : ', num2str(Best_score)]);

        



