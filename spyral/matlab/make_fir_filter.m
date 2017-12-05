% Makes a 512-point band-pss FIR filter using the host-windowing method 
%(Abed & Cain, 1978, The Radio and Electronic Engineer, 46, 293-300).
% The filter is zero-phase (i.e. symmetrical). 
% The function loads in a "host" file, 's1023.ir', which needs to be in the
% current folder.

% arguments are the lower (lo) and high (hi) limits of the band and the
% sampling frequency at which the filter will be used.


function out = make_fir_filter(lo, hi, sf)
nspecs = 1000;
nyquist = sf/2;
file_id = fopen('s1023.ir');
host = fread(file_id,256,'float');
fclose(file_id);
specs = [zeros(1,int32(lo/nyquist*nspecs))];                      % stopband
specs = [specs ones(1,int32(hi/nyquist*nspecs)-length(specs))];   % passband
specs = [specs zeros(1,nspecs-length(specs))];                    % stopband 
band_lo = 0;
win = zeros(1,256);
for i=1:1000
    band_hi = pi*i/nspecs;
    for j=1:256
        b=j-256.5;
        win(j) = win(j) + specs(i) * (sin(b*band_hi) - sin(b*band_lo));
    end
    band_lo = band_hi;
end
out = [host'.*win fliplr(host'.*win)];
