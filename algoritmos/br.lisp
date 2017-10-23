;;;;=================================================
;;;; br.lisp
;;;;
;;;;  Implementacion del algoritmo binary-recursive
;;;;  (br), para la busqueda de testores tipicos.
;;;;
;;;; Ing. Victor Rangel
;;;; Sep, 2017.
;;;;=================================================


(defparameter *tt* nil)

(defparameter *aurora*
  '((1 0 0 0 0 0 0 1 0 )
    (0 1 0 0 0 1 0 0 0 )
    (0 0 0 1 1 1 1 0 1 )
    (0 0 1 0 1 0 0 1 1)
    (1 0 0 0 1 0 0 0 1)))

     
(defun print-data(datos)
  (format t "~{~a~%~}" datos))

(defun reordena(matriz)
  (let ((aux nil)(mat nil)
	(actual 0)(l 1000))
    (loop for i in matriz do
	 (setq actual (reduce #'+ i))
	 (cond ((< actual l)
		(setq l actual aux i))))    
    (setq mat (remove aux matriz :test #'equal))
    (push aux mat)
    (ordena-columna mat)))

(defun ordena-columna(matriz)
  (let ((aux nil)(l (length (car matriz)))
	(m nil))
    (loop for i in (car matriz) for ind below l do
	 (cond ((= i 1) (push ind aux))))
    (loop for renglon in matriz do
	 (loop for el in aux for ind below (length aux) do
	      (setq l (nth (+ ind el ) renglon)
		    renglon (remove l renglon
				    :start (+ el ind) :end (+ 1 el ind)))
	      (push l renglon))
	 (push renglon m))		    
    (list (reverse m) (reverse aux))))

(defun m-identidad(n)
  (let ((aux nil)(cp nil)
	(patron (make-list n :initial-element 0)))
    (loop for i below n do
	 (setq cp (copy-seq patron))
	 (setf (nth i cp) 1)(push  cp aux))
    (reverse aux)))
    
(defun subcon-bin(sub renglon)
  (let ((aux nil))
    (loop for i in sub do
	 (push (nth i renglon) aux))
    (reverse aux)))

(defun tipico?(sub matriz)
  (let ((identidad (m-identidad (length sub)))
	(con-bin nil))
    (labels ((aux(sub id mat)
	       (cond 
		 ((null id) t)((null mat) nil)
		 (t
		  (setq con-bin (subcon-bin sub (car mat)))
		  (aux sub
		       (set-difference id `(,con-bin) :test #'equal)
		       (rest mat))))))
      (aux sub identidad matriz))))

(defun testor?(sub matriz)
  (let ((op 0)(piv 1))
    (loop for row in matriz do
	 (setq op 0)
	 (loop for i in sub do
	      (setq op (boole boole-ior op (nth i row))))
	 (setq piv (boole boole-and piv op))
       until (= piv 0))
    (cond ((= piv 0) nil)(T T))))

(defun cons-sub-start(renglon)
  (let ((l nil))
    (loop for bin in renglon for ind below (length renglon) do
	 (cond ((= bin 1) (push (list ind ) l))))
    (reverse l)))

(defun rm-super(sub L)
  (let ((aux-l nil))
    (loop for i in L do
	 (cond ((null (set-difference
		       sub (intersection sub i :test #'equal)
		       :test #'equal )) nil)
	       (t (push i aux-l))))
    (reverse aux-l)))

(defun add-super(sub L matriz)
  (let ((aux-l (copy-seq (reverse L)))
	(supers nil)(len (1- (length (car matriz))))
	(part nil)
	(ult (car (last sub))))
    (cond ((equal ult len) L)
	  (t
	   (loop for i from (1+ ult) to len do
		(push (append sub `(,i)) supers))
	   (labels ((add-aux ()
		      (cond ((null aux-l)
			     (setq aux-l (append (reverse supers) part)))
			    ((> (length (car aux-l)) 1)
			     (setq aux-l (append supers aux-l))
			     (reverse (append (reverse part) aux-l)))
			    (t (push (pop aux-l) part)
			       (add-aux)))))
	     (add-aux))))))

(defun plus-1(tt)
  (loop for row in tt for i below (length tt) do
       (loop for j below (length row) do
	    (setf (nth j (nth i tt)) (+ (nth j (nth i tt)) 1))))
  tt)

(defun map-original(tt map matriz)
  (let ((lista nil)
	(l-o nil)
	(l-r nil))
    (loop for i below (length (car matriz)) do (push i l-o))
    (setq l-r (append map (set-difference l-o map :test #'equal))
	  lista (pairlis (reverse l-o) l-r))
    (loop for row in tt for i below (length tt) do
       (loop for j below (length row) do
	    (setf (nth j (nth i tt))
		  (cdr (assoc (nth j (nth i tt)) lista)))))
    tt))

        
(defun br(matriz)
  (setq *tt* nil)
  (let* (
	 (map (reordena matriz))
	 (mat (car map))
	 (L (cons-sub-start (car mat)))
	 (sub nil)(tt nil))
    (labels
	((br-aux(L)
	   (cond ((null L)
		  tt)
		 (t
		  (setq sub (pop L))
		  (cond ((tipico? sub mat)
			 (cond ((testor? sub mat)
				(setq L (rm-super sub L))
				(push sub tt)
				(br-aux L))
			       (t
				(setq L (add-super sub L mat))
				(br-aux L))))
			(t
			 (setq L (rm-super sub L))
			 (br-aux L)))))))
      (br-aux L))
    (map-original tt (second map) matriz)
    (setq *tt* (reverse (plus-1 tt)))))
			  	 
