% Generates the upper and lower band cut-offs of a series of 'nbands' contiguous
% frequency bands, linearly spaced on an ERB scale, between the frequencies 
% 'lo' and 'hi' (in Hz)

% e.g. bands = generate_bands(100,8000,20);

function [ bands ] = generate_bands( lo, hi, nbands)
density = nbands/(hz2erb(hi)-hz2erb(lo));
for i=1:nbands
    bands(i,1) = erb2hz(hz2erb(lo)+(i-1)/density);
    bands(i,2) = erb2hz(hz2erb(lo)+i/density);
end

