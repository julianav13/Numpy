      SUBROUTINE FOO(OUT1, OUT2, OUT3, OUT4, OUT5, OUT6)
         CHARACTER SINGLE, DOUBLE, SEMICOL, EXCLA, OPENPAR, CLOSEPAR
         PARAMETER(SINGLE="'", DOUBLE='"', SEMICOL=';', EXCLA="!",
1        OPENPAR = "(", CLOSEPAR = ")")
         CHARACTER OUT1, OUT2, OUT3, OUT4, OUT5, OUT6
         Cf2py intent(out) OUT1, OUT2, OUT3, OUT4, OUT5, OUT6
         OUT1 = SINGLE
         OUT2 = DOUBLE
         OUT3 = SEMICOL
         OUT4 = EXCLA
         OUT5 = OPENPAR
         OUT6 = CLOSEPAR
         RETURN
      END
