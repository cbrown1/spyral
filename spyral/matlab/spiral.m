function out = spiral(ipwave, n_electrodes, n_carriers, spread, sf)
% function out = spiral(ipwave, n_electrodes, n_carriers, spread, sf)
%
% args in: input wave (:,1); number of electrodes; number of tone carriers;
% current spread [in -dB/Oct (negative!!)]; sampling frequency (Hz).
%
%       EXAMPLE: out = spiral(audioread('_wavefilename_'), 20, 80, -8, 44100);
%
% Typical current spread (Oxenham & Kreft 2014 + Nelson etal 2011) = -8 dB/octave.
%
% Author: Jacques Grange, Cardiff Uni, John Culling group, 2017; grangeja@cardiff.ac.uk.
%
    lo=120;                         % lower bound of analysis filters (Hz) (Friesen et al.,2001)
    hi=8658;                        % upper bound of analysis filters (Hz)
    carrier_lo = 20;                % lower bound of carriers (Hz)
    carrier_hi = 20000;             % higher bound of carriers (Hz)
    lp_filter = make_fir_filter(0, 50, sf);                                 % generate low-pass filter,  default 50Hz
    cfs = generate_cfs(lo, hi, n_electrodes);                               % electrodes' centre frequencies
    carrier_fs = generate_cfs(carrier_lo, carrier_hi, n_carriers);          % tone carrier frequencies
    t = 0:1/sf:(length(ipwave)-1)/sf;
    t_carrier = zeros(length(ipwave), n_carriers);
    ip_bands = generate_bands(lo, hi, n_electrodes);                        % lower/upper limits of each analysis band
    ip_bank = zeros(n_electrodes,512);
    envelope = zeros(length(ipwave),n_electrodes);                          % envelopes extracted per electrode
    mixed_envelope = zeros(length(ipwave),n_carriers);                      % mixed envelopes to modulate carriers
    for j=1:n_electrodes            % extraction of envelopes, per analysis band
        ip_bank(j,:) = make_fir_filter(ip_bands(j,1), ip_bands(j,2), sf);   % analysis filterbank
        speechband = conv(ipwave(:,1),ip_bank(j,:),'same')';                % speech band filtering
        speechband = speechband.*(speechband>0);                            % envelope extraction by half-wave rectification
        envelope(:,j) = conv(speechband,lp_filter,'same')';                 % low-pass filter envelope
    end
    for i=1:n_carriers              % contribution of each envelope to each mixed envelope
        for j=1:n_electrodes
            mixed_envelope(:,i) = mixed_envelope(:,i) + ...
          10^(spread/10*abs(log2(cfs(j)/carrier_fs(i))))*envelope(:,j).^2;  % weights applied to power envelopes
        end
    end
    mixed_envelope = mixed_envelope.^0.5;                                   % sqrt to get back to amplitudes
    out = zeros(length(ipwave),1);
    for i=1:n_carriers
        t_carrier(:,i) = sin(2*pi*(carrier_fs(i)*t+rand))';                 % randomise tone phases (particularly important for binaural!)
        out = out + mixed_envelope(:,i).*t_carrier(:,i);                    % modulate carriers with mixed envelopes
    end
    out = out*0.05*sqrt(length(out))/norm(out);                             % rms scaled, to avoid saturation
end



