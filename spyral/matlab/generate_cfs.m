% Generates a series of 'bands' frequencies in Hz, linearely distributed
% on an ERB scale between the frequencies 'lo' and 'hi' (in Hz).
% These would are the centre frequencies (on an ERB scale) of the bands
% specifications made by 'generate_bands' with the same arguments

% e.g. cfs = generate_cfs(100,8000,20);

function [cfs] = generate_cfs( lo, hi, nbands)
density = nbands/(hz2erb(hi)-hz2erb(lo));   %channels per ERB
for i=1:nbands
    cfs(i) = erb2hz(hz2erb(lo)+(i-0.5)/density);
end

