function [ph_out,ph_out_low]=wrap_filt(ph,n_win,alpha,n_pad,low_flag)
%WRAP_FILT Goldstein adaptive and lowpass filtering
%   [ph_out]=wrap_filt(ph,n_win,alpha,n_pad)
%
%   Andy Hooper, June 2006
%   
%   Change Log:
%   07/2006 AH: Added zero padding 
%   02/2012 AH: Set magnitude to original values

if nargin<4 | isempty(n_pad)
    n_pad=round(n_win*0.25);
end

if nargin<5
    low_flag='n';
end
    
[n_i,n_j]=size(ph);
n_inc=floor(n_win/2);
n_win_i=ceil(n_i/n_inc)-1;
n_win_j=ceil(n_j/n_inc)-1;

ph_out=zeros(size(ph));
if strcmpi(low_flag,'y')
    ph_out_low=ph_out;
else
    ph_out_low=[];
end
x=[1:n_win/2];
[X,Y]=meshgrid(x,x);
X=X+Y;
wind_func=[X,fliplr(X)];
wind_func=[wind_func;flipud(wind_func)];


ph(isnan(ph))=0;
B=gausswin(7)*gausswin(7)';
ph_bit=zeros(n_win+n_pad);

L=ifftshift(gausswin(n_win+n_pad,16)*gausswin(n_win+n_pad,16)');

for ix1=1:n_win_i
    wf=wind_func;
    i1=(ix1-1)*n_inc+1;
    i2=i1+n_win-1;
    if i2>n_i
        i_shift=i2-n_i;
        i2=n_i;
        i1=n_i-n_win+1;
        wf=[zeros(i_shift,n_win);wf(1:n_win-i_shift,:)];
    end
    for ix2=1:n_win_j
        wf2=wf;
        j1=(ix2-1)*n_inc+1;
        j2=j1+n_win-1;
        if j2>n_j
           j_shift=j2-n_j;
           j2=n_j;
           j1=n_j-n_win+1;
           wf2=[zeros(n_win,j_shift),wf2(:,1:n_win-j_shift)];
        end
        ph_bit(1:n_win,1:n_win)=ph(i1:i2,j1:j2);
        ph_fft=fft2(ph_bit);
        H=abs(ph_fft);
        H=ifftshift(filter2(B,fftshift(H))); % smooth response
        meanH=median(H(:));
        if meanH~=0
            H=H/meanH;
        end
        H=H.^alpha;
        ph_filt=ifft2(ph_fft.*H);
        ph_filt=ph_filt(1:n_win,1:n_win).*wf2;
        if strcmpi(low_flag,'y')
            ph_filt_low=ifft2(ph_fft.*L);
            ph_filt_low=ph_filt_low(1:n_win,1:n_win).*wf2;
        end
        if isnan(ph_filt(1,1))
            disp('filtered phase contains NaNs in goldstein_filt')
            keyboard
        end
        ph_out(i1:i2,j1:j2)=ph_out(i1:i2,j1:j2)+ph_filt;
        if strcmpi(low_flag,'y')
            ph_out_low(i1:i2,j1:j2)=ph_out_low(i1:i2,j1:j2)+ph_filt_low;
        end
    end
end

ph_out=abs(ph).*exp(j*angle(ph_out)); % reset magnitude
if strcmpi(low_flag,'y')
    ph_out_low=abs(ph).*exp(j*angle(ph_out_low)); % reset magnitude
end


