function position = enforceBounds(position, ub, lb)
    flagUb = position > ub;
    flagLb = position < lb;
    position = position .* ~(flagUb + flagLb) + ub .* flagUb + lb .* flagLb;
end