s|\fbox{\parbox{0.95\textwidth}{\vspace{1.4cm}}}|\framebox[\linewidth]{\rule{0pt}{1.4cm}}|
s|plot (\x,{2.2\*pow(\x,-0.7)}) node\[right\] {\small \$s\,y/k=s\,k^{\alpha-1}\$};|plot (\x,{2.2*pow(\x,-0.7)});\n  \node[right] at (0.75,3.6) {\small $s\,y/k=s\,k^{\alpha-1}$};|
s|\draw\[<->\] (5.2,0.6) -- (5.2,0.97) node\[midway,right\] {\small \$\dot k/k<0\$};|\draw[<->] (5.2,0.71) -- (5.2,0.97);\n  \node[right] at (5.25,0.35) {\small $\dot k/k<0$};|
s|\draw (2.8,3.0) -- (5.2,4.6) node\[right\] {\small pendiente \$=n+\delta\$};|\draw (2.2,3.1) -- (6.2,5.1) node[above] {\small pendiente $=n+\delta$};|
s|\node at (3.1,3.6) {\small pendiente \$g\$ antes y después};|\node at (4.2,0.55) {\small pendiente $g$ antes y después};|
