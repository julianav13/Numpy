        subroutine addb(k)
           real(8), intent(inout) :: k(:)
           k = k + 1
        end subroutine

        subroutine addc(w, k)
           real(8), intent(in) :: w(:)
           real(8), intent(out) :: k(size(w))
           k = w + 1
        end subroutine
